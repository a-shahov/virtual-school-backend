import re
from hashlib import blake2b
from contextlib import suppress
from ipaddress import (
    IPv4Address,
    IPv6Address,
)
from secrets import (
    token_bytes,
    token_urlsafe,
)
from datetime import (
    datetime as dt,
    UTC,
)

import jwt


def generate_hash(password, config, *, salt=None):
    """Generates a hash and a salt and returns them"""

    salt = salt or token_bytes(config.SALT_LEN)
    pass_hash = blake2b(password.encode('utf-8'), key=config.BLAKE2_KEY.encode('utf-8'), salt=salt).digest()
    return pass_hash, salt

def generate_access_token(config, claims):
    """Generates JWT access token"""
    
    payload = {
        'iss': config.BACKEND_NAME,
        'sub': claims['sub'],
        'ueid': claims['ueid'],
        'iat': (timestamp := dt.now(tz=UTC).timestamp()),
        'exp': timestamp + config.ACCESS_TOKEN_EXP,
    }
    token = jwt.encode(
        payload,
        config.TOKEN_KEY,
        algorithm=config.TOKEN_ALG,
    )
    
    return token, payload

def generate_refresh_token(config, claims):
    """Generates JWT refresh token"""

    # TODO: need to add method update
    payload = {
        'iss': config.BACKEND_NAME,
        'sub': claims['sub'],
        'ueid': claims['ueid'],
        'jti': token_urlsafe(config.JTI_LEN),
        'iat': (timestamp := dt.now(tz=UTC).timestamp()),
        'exp': claims.get('exp', timestamp + config.REFRESH_TOKEN_EXP),
    }
    token = jwt.encode(
        payload,
        config.TOKEN_KEY,
        algorithm=config.TOKEN_ALG,
    )
    
    return token, payload

def _validate_ip(value):
    """
    return True if value valid ipv4 or ipv6 address otherwise return False
    """
    with suppress(ValueError):
        if IPv4Address(value):
            return True

    with suppress(ValueError):
        if IPv6Address(value):
            return True

    return False

def validate_email(email_address):
    """return True if email_address is valid otherwise False"""

    HOST_REGEXP = re.compile(
        # max length for domain name labels is 63 characters per RFC 1034
        r'((?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+)' +
        r'(?:[A-Z0-9-]{2,63}(?<!-))\Z',
        re.IGNORECASE,
    )

    LITERAL_REGEXP = re.compile(
        # literal form, ipv4 or ipv6 address (SMTP 4.1.3)
        r'\[([A-F0-9:\.]+)\]\Z',
        re.IGNORECASE,
    )

    USER_REGEXP = re.compile(
        # dot-atom
        r"(^[-!#$%&'*+/=?^_`{}|~0-9A-Z]+(\.[-!#$%&'*+/=?^_`{}|~0-9A-Z]+)*\Z" +
        # quoted-string
        r'|^"([\001-\010\013\014\016-\037!#-\[\]-\177]|\\[\001-\011\013' +
        r'\014\016-\177])*"\Z)',
        re.IGNORECASE,
    )

    try:
        user, domain = email_address.rsplit('@', 1)
    except ValueError:
        return False

    if not USER_REGEXP.match(user):
        return False

    if domain.startswith('[') and domain.endswith(']'):
        literal_match = LITERAL_REGEXP.match(domain)
        if literal_match is None:
            return False
        elif not _validate_ip(literal_match.group(1)):
            return False
    else:
        if not HOST_REGEXP.match(domain):
            return False

    return True