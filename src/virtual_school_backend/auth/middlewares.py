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

@middleware
async def refresh_middleware(request, handler):
    refresh_endpoints = [
        ('GET', '/auth/logout'),
        ('GET', '/auth/refresh'),
    ]
    if (request.method, request.url.path) not in refresh_endpoints:
        return await handler(request)
    
    config = request.app[ROOT_APP][CONFIG]
    
    if not (refresh_token := request.cookies.get('__Secure-refresh-token')):
        raise HTTPUnauthorized(reason='the refresh token is missing in request')
    
    try:
        refresh_payload = jwt.decode(
            refresh_token, config.TOKEN_KEY,
            algorithms=config.TOKEN_ALG,
            require=config.REFRESH_TOKEN_CLAIMS,
            issuer=config.BACKEND_NAME,
        )
    except ExpiredSignatureError:
        raise HTTPForbidden(reason='the refresh token has expired')
    except InvalidSignatureError:
        raise HTTPUnauthorized(reason='invalid refresh token')
    
    request['refresh_payload'] = refresh_payload
    return await handler(request)
