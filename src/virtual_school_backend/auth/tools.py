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


def generate_hash(password, config, *, salt=None):
    """
    Generates a hash and a salt and returns them.
    """
    salt = salt or token_bytes(config.SALT_LEN)
    print('gen hash', salt)
    pass_hash = blake2b(password.encode(), key=config.PASS_KEY.encode(), salt=salt).digest()
    print('gen hash', pass_hash)
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

