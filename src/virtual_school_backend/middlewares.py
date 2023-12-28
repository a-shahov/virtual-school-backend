from aiohttp.web import (
    middleware,
    HTTPForbidden,
    HTTPUnauthorized,
)
import jwt
from jwt import (
    ExpiredSignatureError,
    InvalidSignatureError,
)

from virtual_school_backend.appkeys import (
    CONFIG,
    ROOT_APP,
)


def set_permission(permisions):
    valid_perms = ('admin', 'teacher', 'user')
    assert all((perm in valid_perms for perm in permisions)), f'this {permisions}, are not valid'

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
    pass