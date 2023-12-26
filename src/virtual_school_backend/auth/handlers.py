from aiohttp.web import (
    View,
    Response,
    json_response,
    HTTPBadRequest,
)
import jwt

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

#  TODO: NEED cerberus
LOGIN_SCHEME = ''
REFRESH_SCHEME = ''
REGISTRATION_SCHEME = ''

LOGIN_QUERY_SELECT = """
    SELECT id, role, password, salt
        FROM login
        WHERE email = %s;
"""
#  SELECT extract( epoch from date_trunc('seconds', now()) at time zone 'utc')::numeric(20)
LOGIN_QUERY_INSERT = """
    INSERT INTO tokens ( login_id, token, jti, exp )
        VALUES ( %s, %s, %s, %s );
"""
REGISTRATION_QUERY = ''
REFRESH_QUERY = ''
LOGOUT_QUERY = ''


class LoginHandler(View):

    @validate_json_request(LOGIN_SCHEME)
    async def post(self, body):
        config = self.request.app[ROOT_APP][CONFIG]
        pg_pool = self.request.app[ROOT_APP][PG_POOL]

        async with pg_pool.connection() as conn:
            async with conn.cursor() as acur:

                await acur.execute(LOGIN_QUERY_SELECT, (body['email'],))
                if not (result := await acur.fetchone()):
                    raise HTTPBadRequest(reason='email not in database')

                login_id, role, password_db, salt = result
                password = generate_hash(
                    body['password'], config.PASS_KEY, salt=salt,
                )

                if password != password_db:
                    #raise HTTPBadRequest(reason='wrong password')
                    ...
                                    
                access_token = generate_access_token(config, {'sub': role})
                access_payload = jwt.decode(
                    access_token, config.TOKEN_KEY,
                    algorithms=config.TOKEN_ALG,
                )

                refresh_token = generate_refresh_token(config)
                refresh_payload = jwt.decode(
                    refresh_token, config.TOKEN_KEY,
                    algorithms=config.TOKEN_ALG,
                )

                await acur.execute(
                    LOGIN_QUERY_INSERT,
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
                'role': role,
                'access_token': access_token,
                'expires_in': expires_in,
                'expires': round(refresh_payload['exp']),
            }
        )
        response.set_cookie(
            '__Secure-refresh-token', refresh_token,
            path='/auth/refresh', httponly=True,
            secure=True, samesite='Strict',
        )
        return response

class RefreshHandler(View):
    @validate_json_request(REFRESH_SCHEME)
    async def post(self, body):
        return Response(text='refresh')


class RegistrationHandler(View):
    @validate_json_request(REGISTRATION_SCHEME)
    async def post(self, body):
        return Response(text='registration')


class LogoutHandler(View):
    async def get(self):
        return Response(text='logout')


class WhoamiHandler(View):
    async def get(self):
        return Response(text='whoami')
