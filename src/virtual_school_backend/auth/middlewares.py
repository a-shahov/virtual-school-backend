import logging

from aiohttp.web import (
    middleware,
    HTTPForbidden,
    HTTPUnauthorized,
)
import jwt
from jwt import (
    ExpiredSignatureError,
    InvalidSignatureError,
    InvalidIssuedAtError,
    InvalidIssuerError,
    InvalidTokenError,
    ImmatureSignatureError,
)

from virtual_school_backend.appkeys import CONFIG

log = logging.getLogger('aiohttp.web')


@middleware
async def refresh_middleware(request, handler):
    """This middleware validates refresh token for specified paths"""
    refresh_endpoints = [
        ('GET', '/auth/logout'),
        ('GET', '/auth/refresh'),
    ]
    if (request.method, request.url.path) not in refresh_endpoints:
        return await handler(request)
    
    config = request.config_dict[CONFIG]
    
    if not (refresh_token := request.cookies.get('__Secure-refresh-token')):
        raise HTTPUnauthorized(reason='the refresh token is missing in request')
    
    try:
        refresh_payload = jwt.decode(
            refresh_token, config.TOKEN_KEY,
            algorithms=config.TOKEN_ALG,
            issuer=config.BACKEND_NAME,
            options={
                'verify_signature': True,
                'require': config.REFRESH_TOKEN_CLAIMS,
            },
        )
    except ExpiredSignatureError:
        raise HTTPForbidden(reason='the refresh token has expired')
    except InvalidSignatureError:
        raise HTTPUnauthorized(reason='invalid refresh token signature')
    except InvalidIssuerError:
        raise HTTPUnauthorized(reason='invalid iss claim in refresh token')
    except InvalidIssuedAtError:
        raise HTTPUnauthorized(reason='invalid iat claim in refresh token')
    except ImmatureSignatureError:
        raise HTTPForbidden(reason='iat claim in the future in refresh token')
    except InvalidTokenError as err:
        if log.isEnabledFor(logging.DEBUG):
            log.debug(
                'jwt decode error = %s %s', err, type(err),
                extra={'url': request.rel_url, 'method': request.method},
            )
        raise HTTPUnauthorized(reason='invalid refresh token')
    
    if not isinstance(refresh_payload['ueid'], int):
        raise HTTPUnauthorized(reason='invalid ueid claim in refresh token')

    request['refresh_payload'] = refresh_payload

    if log.isEnabledFor(logging.DEBUG):
        log.debug(
            'refresh payload: %s', refresh_payload,
            extra={'url': request.rel_url, 'method': request.method},
        )

    return await handler(request)
