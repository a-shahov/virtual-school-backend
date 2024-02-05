import logging
from dataclasses import dataclass
from datetime import (
    date,
    datetime as dt,
    timezone as tz,
)

from aiohttp.web import (
    View,
    Response,
    json_response,
    HTTPBadRequest,
    HTTPUnauthorized,
    HTTPForbidden,
)
import jwt
from jwt import (
    ExpiredSignatureError,
    InvalidSignatureError,
)

from virtual_school_backend import (
    CONFIG,
    PG_POOL,
    validate_json_request,
)
from .validation_schemas import (
    REGISTRATION_SCHEMA,
    LOGIN_SCHEMA,
    registration_formatcheck,
    login_formatcheck,
)
from .tools import (
    generate_hash,
    generate_access_token,
    generate_refresh_token,
)

log = logging.getLogger('aiohttp.web')


# TODO: need rewrite all SQL queries
SELECT_LOGIN_BY_EMAIL = """
    SELECT
        l.id, l.role,
        l.password, l.salt,
        l.email, u.state, u.name,
        u.secondname, u.patronymic,
        u.birthdate, u.phone, u.class
      FROM login l
      LEFT OUTER JOIN user_account u ON u.login_id = l.id
      WHERE l.email = %s;
"""

@dataclass(frozen=True)
class LoginData:
    login_id: int
    role: str
    pass_hash: str
    salt: str
    email: str
    state: str
    name: str
    secondname: str
    patronymic: str
    birthdate: date
    phone: str
    class_n: int

#  SELECT extract( epoch from date_trunc('seconds', now()) at time zone 'utc')::numeric(20)
INSERT_TOKENS = """
    INSERT INTO tokens ( login_id, token, jti, exp )
        VALUES ( %s, %s, %s, %s );
"""
SELECT_USER = """
    SELECT phone, name, secondname, patronymic
        FROM user_account
        WHERE phone = %s OR
        name = %s AND secondname = %s
        AND patronymic = %s;
"""
INSERT_LOGIN = """
    INSERT INTO login ( role, email, password, salt )
        VALUES ( %s, %s, %b, %b )
"""
INSERT_USER = """
    INSERT INTO user_account ( 
        login_id, state, name, secondname, 
        patronymic, birthdate, phone, class
        )
        VALUES ( %s, %s, %s, %s, %s, %s, %s, %s);
"""
SELECT_USER_BY_ID = """
    SELECT id FROM user_account
        WHERE login_id = %s
"""
UPDATE_LOGIN = """
    UPDATE login
        SET user_id = %s WHERE id = %s;
"""
SELECT_TOKENS = """
    SELECT login_id, used FROM tokens
        WHERE jti = %s;
"""
UPDATE_TOKEN_USED = """
    UPDATE tokens
        SET used = true WHERE jti = %s;
"""


class LoginHandler(View):
    """View for /auth/login"""

    @validate_json_request(LOGIN_SCHEMA, login_formatcheck)
    async def post(self, json_data):
        config = self.request.config_dict[CONFIG]
        pg_pool = self.request.config_dict[PG_POOL]

        async with pg_pool.connection() as conn:
            async with conn.cursor() as acur:

                await acur.execute(SELECT_LOGIN_BY_EMAIL, (json_data['email'],))
                if not (result := await acur.fetchone()):
                    raise HTTPBadRequest(reason='email not in database')

                login_data = LoginData(*result)
                pass_hash, unused = generate_hash(
                    json_data['password'], config, salt=login_data.salt,
                )

                if pass_hash != login_data.pass_hash:
                    raise HTTPBadRequest(reason='wrong password')

                claims = {'sub': login_data.role, 'ueid': login_data.login_id} 
                access_token, access_payload = generate_access_token(config, claims)
                refresh_token, refresh_payload = generate_refresh_token(config, claims)

                await acur.execute(
                    INSERT_TOKENS,
                    (
                        login_data.login_id,
                        refresh_token,
                        refresh_payload['jti'],
                        refresh_payload['exp'],
                    ),
                )
                #  TODO: update timestamps in db
                #  TODO: need delete rotten tokens
        
        expires_in = round(access_payload['exp'] - access_payload['iat'])
        response = json_response(
            {
                'role': access_payload['sub'],
                'token': {
                    'token_type': 'Bearer',
                    'access_token': access_token,
                    'expires_in': expires_in,
                    'expires': round(refresh_payload['exp']),
                },
                'user_info': {
                    'login_id': access_payload['ueid'],
                    'state': login_data.state,
                    'email': login_data.email,
                    'name': login_data.name,
                    'secondname': login_data.secondname,
                    'patronymic': login_data.patronymic,
                    'birthdate': login_data.birthdate.isoformat(),
                    'phone': login_data.phone,
                    'class': int(login_data.class_n),
                },
            }
        )
        response.set_cookie(
            '__Secure-refresh-token', refresh_token,
            path='/auth/', httponly=True,
            secure=True, samesite='None',
            max_age=round(refresh_payload['exp'] - refresh_payload['iat']),
        )

        log.info('User has logged in with email: %s', json_data['email'])

        return response

class RefreshHandler(View):
    """View for /auth/refresh"""

    async def get(self):
        config = self.request.config_dict[CONFIG]
        pg_pool = self.request.config_dict[PG_POOL]
        refresh_payload = self.request['refresh_payload']
        
        async with pg_pool.connection() as conn:
            async with conn.cursor() as acur:

                await acur.execute(SELECT_TOKENS, (refresh_payload['jti'],))
                if (result := await acur.fetchone()):
                    login_id, token_used = result
                else:
                    raise HTTPUnauthorized(reason='token not in database')
                
                if token_used:
                    raise HTTPForbidden(reason='the token was used')
                
                await acur.execute(UPDATE_TOKEN_USED, (refresh_payload['jti'],))

                new_refresh_token, new_refresh_payload = generate_refresh_token(
                    config, 
                    {
                        'sub': refresh_payload['sub'],
                        'ueid': refresh_payload['ueid'],
                        'exp': refresh_payload['exp'],
                    }
                )
                new_access_token, new_access_payload = generate_access_token(
                    config, 
                    {'sub': refresh_payload['sub'], 'ueid': refresh_payload['ueid']},
                )

                await acur.execute(
                    INSERT_TOKENS,
                    (
                        login_id,
                        new_refresh_token,
                        new_refresh_payload['jti'],
                        new_refresh_payload['exp'],
                    ),
                )

        expires_in = round(new_access_payload['exp'] - new_access_payload['iat'])
        response = json_response(
            {
                'token_type': 'Bearer',
                'access_token': new_access_token,
                'role': new_access_payload['sub'],
                'login_id': new_access_payload['ueid'],
                'expires_in': expires_in,
                'expires': round(new_refresh_payload['exp']),
            }
        )
        response.set_cookie(
            '__Secure-refresh-token', new_refresh_token,
            path='/auth/', httponly=True,
            secure=True, samesite='None',
            max_age=round(new_refresh_payload['exp'] - new_refresh_payload['iat']),
        )

        return response


class RegistrationHandler(View):
    """View for /auth/registration"""

    @validate_json_request(REGISTRATION_SCHEMA, registration_formatcheck)
    async def post(self, json_data):
        config = self.request.config_dict[CONFIG]
        pg_pool = self.request.config_dict[PG_POOL]

        async with pg_pool.connection() as conn:
            async with conn.cursor() as acur:
             
                await acur.execute(SELECT_LOGIN_BY_EMAIL, (json_data['email'],))
                if await acur.fetchone():
                    raise HTTPBadRequest(reason='email already exists')
                
                await acur.execute(
                    SELECT_USER,
                    (
                        json_data['phone'],
                        json_data['name'],
                        json_data['secondname'],
                        json_data['patronymic'],
                    ),
                )
                if (result := await acur.fetchone()):
                    # TODO: dataclasses or pydantic or attrs? for result
                    # TODO: work with enum?
                    phone, *unused = result
                    if phone == json_data['phone']:
                        raise HTTPBadRequest(reason='phone number already exists')
                    raise HTTPBadRequest(reason='user already exists')

                await acur.execute(INSERT_LOGIN, (
                    'user',
                    json_data['email'],
                    *generate_hash(json_data['password'], config),
                ))

                await acur.execute(SELECT_LOGIN_BY_EMAIL, (json_data['email'],))
                login_id, *unused = await acur.fetchone()

                await acur.execute(INSERT_USER, (
                    login_id,
                    'new',
                    json_data['name'],
                    json_data['secondname'],
                    json_data['patronymic'],
                    json_data['birthdate'],
                    json_data['phone'],
                    json_data['class'],
                ))

                await acur.execute(SELECT_USER_BY_ID, (login_id,))
                user_id, = await acur.fetchone()

                await acur.execute(UPDATE_LOGIN, (user_id, login_id))

        log.info(
            'New user %s %s with email: %s has registered',
            json_data['name'], json_data['secondname'], json_data['email'],
        )
                
        return Response()


class LogoutHandler(View):
    """View for /auth/logout"""

    async def get(self):
        pg_pool = self.request.config_dict[PG_POOL]
        refresh_payload = self.request['refresh_payload']

        async with pg_pool.connection() as conn:
            async with conn.cursor() as acur:

                await acur.execute(SELECT_TOKENS, (refresh_payload['jti'],))
                if (result := await acur.fetchone()):
                    login_id, token_used = result
                else:
                    raise HTTPUnauthorized(reason='token not in database')
                
                if token_used:
                    raise HTTPForbidden(reason='the token was used')

                await acur.execute(UPDATE_TOKEN_USED, (refresh_payload['jti'],))
        
        response = Response()
        response.set_cookie(  # del_cookie doesnt work with secure
            '__Secure-refresh-token', '', path='/auth/', 
            max_age=0, httponly=True, secure=True, 
            samesite='None',
        )

        return response
