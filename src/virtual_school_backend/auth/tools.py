from hashlib import blake2b
from secrets import (
    token_bytes,
    token_urlsafe,
)
from datetime import (
    datetime as dt,
    timezone as tz,
    timedelta
)

import jwt


def generate_hash(data, key, *, salt_len=None, salt=None):
    """
    Generates a hash and a salt and returns them.
    If salt is not None then does not generate new salt with salt_len.
    """
    assert salt or salt_len, 'salt or salt_len must be specified'
    salt = salt or token_bytes(salt_len)
    pass_hash = blake2b(data.encode(), key=key.encode(), salt=salt).digest()

    return pass_hash, salt

def generate_access_token(config, claims):
    """Generates JWT access token"""
    token = jwt.encode(
        {
            'iss': config.BACKEND_NAME,
            'sub': claims['sub'],
            'iat': (timestamp := dt.now(tz=tz.utc).timestamp()),
            'exp': timestamp + config.ACCESS_TOKEN_EXP,
        },
        config.TOKEN_KEY,
        algorithm=config.TOKEN_ALG,
    )
    
    return token

def generate_refresh_token(config, claims={}):
    """
    Generates JWT refresh token.
    If 'jti' not in claims, generates new jti.
    """
    token = jwt.encode(
        {
            'iss': config.BACKEND_NAME,
            'jti': claims.get('jti', token_urlsafe(config.JTI_LEN)),
            'iat': (timestamp := dt.now(tz=tz.utc).timestamp()),
            'exp': timestamp + config.REFRESH_TOKEN_EXP,
        },
        config.TOKEN_KEY,
        algorithm=config.TOKEN_ALG,
    )
    
    return token

