from datetime import (
    datetime as dt,
    timezone as tz,
)

from aiohttp.web import (
    View,
    Response,
    json_response,
    HTTPBadRequest,
    HTTPOk,
    HTTPUnauthorized,
)
import jwt
from jwt import ExpiredSignatureError

from virtual_school_backend import (
    ROOT_APP,
    CONFIG,
    PG_POOL,
    validate_json_request,
)
from .tools import (
    generate_hash,
    generate_access_token,
    generate_refresh_token,
)

# TODO: NEED cerberus
LOGIN_SCHEME = ''
REFRESH_SCHEME = ''
REGISTRATION_SCHEME = ''

# TODO: need rewrite all SQL queries
SELECT_LOGIN_BY_EMAIL = """
    SELECT id, role, password, salt
        FROM login
        WHERE email = %s;
"""
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
    INSERT INTO user_account ( login_id, state, name, secondname, patronymic, phone, class)
        VALUES ( %s, %s, %s, %s, %s, %s, %s);
"""
SELECT_USER_BY_ID = """
    SELECT id FROM user_account
        WHERE login_id = %s;
"""
UPDATE_LOGIN = """
    UPDATE login
        SET user_id = %s WHERE id = %s;
"""
SELECT_TOKENS = """
    SELECT login_id, used FROM tokens
        WHERE jti = %s;
"""
UPDATE_TOKENS = """
    UPDATE tokens
        SET used = true WHERE jti = %s;
"""
dir(__file__)

class LoginHandler(View):

    @validate_json_request(LOGIN_SCHEME)
    async def post(self, json_data):
        config = self.request.app[ROOT_APP][CONFIG]
        pg_pool = self.request.app[ROOT_APP][PG_POOL]

        async with pg_pool.connection() as conn:
            async with conn.cursor() as acur:

                await acur.execute(SELECT_LOGIN_BY_EMAIL, (json_data['email'],))
                if not (result := await acur.fetchone()):
                    raise HTTPBadRequest(reason='email not in database')

                login_id, role, pass_hash_db, salt = result
                pass_hash, unused = generate_hash(
                    json_data['password'], config, salt=salt,
                )

                if pass_hash != pass_hash_db:
                    raise HTTPBadRequest(reason='wrong password')
                                    
                access_token = generate_access_token(config, {'sub': role})
                access_payload = jwt.decode(
                    access_token, config.TOKEN_KEY,
                    algorithms=config.TOKEN_ALG,
                )

                refresh_token = generate_refresh_token(config, {'sub': role})
                refresh_payload = jwt.decode(
                    refresh_token, config.TOKEN_KEY,
                    algorithms=config.TOKEN_ALG,
                )

                await acur.execute(
                    INSERT_TOKENS,
                    (
                        login_id,
                        refresh_token,
                        refresh_payload['jti'],
                        refresh_payload['exp'],
                    ),
                )
                #  TODO: update timestamp in db
                #  TODO: need delete rotten tokens
        
        expires_in = round(access_payload['exp'] - access_payload['iat'])
        response = json_response(
            {
                'token_type': 'Bearer',
                'access_token': access_token,
                'expires_in': expires_in,
                'expires': round(refresh_payload['exp']),
            }
        )
        response.set_cookie(
            '__Secure-refresh-token', refresh_token,
            path='/auth/', httponly=True,
            secure=True, samesite='Strict',
            max_age=round(refresh_payload['exp'] - refresh_payload['iat']),
        )
        return response

class RefreshHandler(View):
    async def get(self):
        pg_pool = self.request.app[ROOT_APP][PG_POOL]
        config = self.request.app[ROOT_APP][CONFIG]

        # TODO: move to middleware
        if not (refresh_token := self.request.cookies.get('__Secure-refresh-token')):
            raise HTTPUnauthorized(reason='the refresh token is missing in request')
        
        try:
            refresh_payload = jwt.decode(
                refresh_token, config.TOKEN_KEY,
                algorithms=config.TOKEN_ALG,
            )
        except ExpiredSignatureError as err:
            raise HTTPUnauthorized(reason='the refresh token has expired')
        
        async with pg_pool.connection() as conn:
            async with conn.cursor() as acur:

                await acur.execute(SELECT_TOKENS, (refresh_payload['jti'],))
                if (result := await acur.fetchone()):
                    login_id, token_used = result
                else:
                    raise HTTPUnauthorized(reason='invalid token')
                
                if token_used:
                    raise HTTPUnauthorized(reason='the token was used')
                
                await acur.execute(UPDATE_TOKENS, (refresh_payload['jti'],))

                new_refresh_token = generate_refresh_token(
                    config, 
                    {
                        'sub': refresh_payload['sub'],
                        'exp': refresh_payload['exp'],
                    }
                )
                new_refresh_payload = jwt.decode(
                    new_refresh_token, config.TOKEN_KEY,
                    algorithms=config.TOKEN_ALG,
                )

                new_access_token = generate_access_token(
                    config, {'sub': refresh_payload['sub']},
                )
                new_access_payload = jwt.decode(
                    new_access_token, config.TOKEN_KEY,
                    algorithms=config.TOKEN_ALG,
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
                'expires_in': expires_in,
                'expires': round(new_refresh_payload['exp']),
            }
        )
        response.set_cookie(
            '__Secure-refresh-token', new_refresh_token,
            path='/auth/', httponly=True,
            secure=True, samesite='Strict',
            max_age=round(new_refresh_payload['exp'] - new_refresh_payload['iat']),
        )

        return response


class RegistrationHandler(View):
    @validate_json_request(REGISTRATION_SCHEME)
    async def post(self, json_data):
        pg_pool = self.request.app[ROOT_APP][PG_POOL]
        config = self.request.app[ROOT_APP][CONFIG]

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
                    json_data['phone'],
                    json_data['class'],
                ))

                await acur.execute(SELECT_USER_BY_ID, (login_id,))
                user_id, = await acur.fetchone()

                await acur.execute(UPDATE_LOGIN, (user_id, login_id))
                
        return Response()


class LogoutHandler(View):
    async def get(self):
        pg_pool = self.request.app[ROOT_APP][PG_POOL]
        config = self.request.app[ROOT_APP][CONFIG]

        if not (refresh_token := self.request.cookies.get('__Secure-refresh-token')):
            raise HTTPOk(reason='the refresh token is missing in request')
        
        try:
            refresh_payload = jwt.decode(
                refresh_token, config.TOKEN_KEY,
                algorithms=config.TOKEN_ALG,
            )
        except ExpiredSignatureError:
            raise HTTPOk(reason='the refresh token has expired')

        async with pg_pool.connection() as conn:
            async with conn.cursor() as acur:

                await acur.execute(UPDATE_TOKENS, (refresh_payload['jti'],))

        return Response()
