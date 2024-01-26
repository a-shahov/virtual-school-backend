import logging
import sys
import traceback

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
    InvalidIssuedAtError,
    InvalidIssuerError,
    InvalidTokenError,
    ImmatureSignatureError,
)

from virtual_school_backend.appkeys import CONFIG

log = logging.getLogger('aiohttp.web')


def set_permission(permisions):
    """This functions is used as decorator which sets permissions on handlers"""
    valid_perms = {'admin', 'teacher', 'user'}
    assert all((perm in valid_perms for perm in permisions)), f'this {permisions=}, are not valid'

    def wrapper(func):
        func.permissions = permisions
        return func
    return wrapper

@middleware
async def auth_middleware(request, handler):
    """
    Retrieve and validate access token from Authorization header
    And then check sub claim according to handler permissions
    """
    config = request.app[CONFIG]

    if log.isEnabledFor(logging.DEBUG):
        log.debug(
            'headers: %s', request.headers,
            extra={'url': request.rel_url, 'method': request.method},
        )

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
            issuer=config.BACKEND_NAME,
            options={
                'verify_signature': True,
                'require': config.ACCESS_TOKEN_CLAIMS,
            },
        )
    except ExpiredSignatureError:
        raise HTTPForbidden(reason='the access token has expired')
    except InvalidSignatureError:
        raise HTTPUnauthorized(reason='invalid access token signature')
    except InvalidIssuerError:
        raise HTTPUnauthorized(reason='invalid iss claim in access token')
    except InvalidIssuedAtError:
        raise HTTPUnauthorized(reason='invalid iat claim in access token')
    except ImmatureSignatureError:
        raise HTTPForbidden(reason='iat claim in the future in access token')
    except InvalidTokenError as err:
        if log.isEnabledFor(logging.DEBUG):
            log.debug(
                'jwt decode error = %s %s', err, type(err),
                extra={'url': request.rel_url, 'method': request.method},
            )
        raise HTTPUnauthorized(reason='invalid access token')
    
    if log.isEnabledFor(logging.DEBUG):
        log.debug(
            'access token payload: [%s]', access_payload,
            extra={'url': request.rel_url, 'method': request.method},
        )

    if access_payload['sub'] not in permissions and access_payload['sub'] != 'admin':
        raise HTTPForbidden(reason='insufficient access rights')

    return await handler(request)

@middleware
async def error_middleware(request, handler):
    """Intercepts exceptions and returns json with errors"""
    try:
        exc = None
        response = await handler(request)
    except HTTPException as err:
        response = json_response(
            {'errors': [err.reason]},
            status=err.status_code,
        )
        exc = sys.exc_info()[1]
    except ExceptionGroup as err:  # ExceptionGroup only for validation errors
        response = json_response(
            {'errors': [exc.reason for exc in err.exceptions]},
            status=400,
        )
        exc = sys.exc_info()[1]
    finally:
        if exc and log.isEnabledFor(logging.DEBUG):
            log.debug(
                'exception:\n%s', "".join(traceback.format_exception(exc)),
                extra={'url': request.rel_url, 'method': request.method},
            )

    return response