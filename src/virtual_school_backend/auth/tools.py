from hashlib import blake2b
from secrets import (
    token_bytes,
    token_urlsafe,
)
from datetime import (
    datetime as dt,
    timezone as tz,
)

import jwt


def generate_hash(password, config, *, salt=None):
    """
    Generates a hash and a salt and returns them.
    """
    salt = salt or token_bytes(config.SALT_LEN)
    pass_hash = blake2b(password.encode('utf-8'), key=config.PASS_KEY.encode('utf-8'), salt=salt).digest()
    return pass_hash, salt

def generate_access_token(config, claims):
    """Generates JWT access token"""
    
    payload = {
        'iss': config.BACKEND_NAME,
        'sub': claims['sub'],
        'iat': (timestamp := dt.now(tz=tz.utc).timestamp()),
        'exp': timestamp + config.ACCESS_TOKEN_EXP,
    }
    token = jwt.encode(
        payload,
        config.TOKEN_KEY,
        algorithm=config.TOKEN_ALG,
    )
    
    return token, payload

def generate_refresh_token(config, claims):
    """Generates JWT refresh token."""

    payload = {
        'iss': config.BACKEND_NAME,
        'sub': claims['sub'],
        'jti': token_urlsafe(config.JTI_LEN),
        'iat': (timestamp := dt.now(tz=tz.utc).timestamp()),
        'exp': claims.get('exp', timestamp + config.REFRESH_TOKEN_EXP),
    }
    token = jwt.encode(
        payload,
        config.TOKEN_KEY,
        algorithm=config.TOKEN_ALG,
    )
    
    return token, payload

