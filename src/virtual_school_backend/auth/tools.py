from hashlib import blake2b
from secrets import token_bytes
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

def generate_token(iss, sub, exp, key, algorithm):
    """Generates JWT token"""
    token = jwt.encode(
        {
            'iss': iss,
            'sub': sub,
            'iat': (timestamp := round(dt.now(tz=tz.utc).timestamp())),
            'exp': timestamp + exp,
        },
        key,
        algorithm=algorithm,
    )
    
    return token
