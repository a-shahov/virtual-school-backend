from aiohttp.web import (
    json_response,
    middleware,
    HTTPException,
    HTTPForbidden,
    HTTPUnauthorized,
)
import jwt
from jwt import (
    ExpiredSignatureError,
    InvalidSignatureError,
)

from virtual_school_backend.appkeys import CONFIG


def set_permission(permisions):
    valid_perms = ('admin', 'teacher', 'user')
    assert all((perm in valid_perms for perm in permisions)), f'this {permisions=}, are not valid'

    def wrapper(func):
        func.permissions = permisions
        return func
    return wrapper

@middleware
async def auth_middleware(request, handler):
    config = request.app[CONFIG]

    endpoint = getattr(handler, request.method.lower(), None)
    permissions = getattr(endpoint, 'permissions', None)
    if not permissions:
        return await handler(request)
    
    if not (bearer_token := request.headers.get('Authorization')):
        raise HTTPUnauthorized(reason='the access token is missing')
    
    try:
        token_type, access_token = bearer_token.split()
    except ValueError:
        raise HTTPUnauthorized('invalid access token')

    if token_type != 'Bearer':
        raise HTTPUnauthorized('invalid token type, must be "Bearer"')

    try:
        access_payload = jwt.decode(
            access_token, config.TOKEN_KEY,
            algorithms=config.TOKEN_ALG, 
            require=config.ACCESS_TOKEN_CLAIMS,
            issuer=config.BACKEND_NAME,
        )
    except ExpiredSignatureError:
        raise HTTPForbidden(reason='the access token has expired')
    except InvalidSignatureError:
        raise HTTPUnauthorized(reason='invalid access token')

    if access_payload['sub'] not in permissions and access_payload['sub'] != 'admin':
        raise HTTPForbidden(reason='insufficient access rights')

    return await handler(request)

@middleware
async def error_middleware(request, handler):
    try:
        response = await handler(request)
    except HTTPException as err:
        response = json_response(
            {'errors': [err.reason]},
            status=err.status_code,
        )
    except ExceptionGroup as err:
        response = json_response(
            {'errors': [(exc.cause.message if exc.cause else exc.message) for exc in err.exceptions]},
            status=400,
        )
    except Exception as err:
        raise err

    return response