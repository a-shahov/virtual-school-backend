import os
import tomllib
from pathlib import Path
import string

from dotenv import load_dotenv


# Load .env file in environment
load_dotenv(Path(__file__).parents[1] / '.env')

# Load pyproject.toml
with Path(__file__).parents[3].joinpath('pyproject.toml').open('rb') as toml_f:
    pyproj_toml = tomllib.load(toml_f)

# Load logging.toml with logging config
with Path(__file__).with_name('logging.toml').open('rb') as toml_f:
    log_toml = tomllib.load(toml_f)


class Config:
    """Class for storing full backend configuration"""

    # General backend settings
    BACKEND_NAME = pyproj_toml['project']['name']
    STARTUP_MODE = os.getenv('STARTUP_MODE').lower()
    HOST = os.getenv('HOST')
    PORT = int(os.getenv('PORT'))

    # Database connection
    DSN = (
        f'dbname={os.getenv("PG_NAME")} '
        f'user={os.getenv("PG_USER")} '
        f'host={os.getenv("PG_HOST")} '
        f'port={os.getenv("PG_PORT")} '
        f'password={os.getenv("PG_PASSWORD")}'
    )

    # Logging settings
    LOGGING_INFO = log_toml['logging_info']
    LOGGING_DEBUG = log_toml['logging_debug']
    ACCESS_LOG_FMT = log_toml['access_logger']['format']

    # Password cryptography settings
    PASS_KEY = os.getenv('BLAKE2_KEY')  # key for generate password hash (blake2b)
    SALT_LEN = 8  # from 0 to 16 bytes for blake2b
    # TODO: replace with regexp
    PASS_MUST_SUBSETS_CHARS = [
        frozenset(string.ascii_lowercase),
        frozenset(string.ascii_uppercase),
        frozenset(string.digits),
    ]
    PASS_VALID_CHARS = [
        *PASS_MUST_SUBSETS_CHARS,
        frozenset(string.punctuation),
    ]
    PASS_FORBID_CHARS = [
        frozenset(string.whitespace),
    ]

    # JWT token settings
    TOKEN_KEY = os.getenv('TOKEN_KEY')  # key for generate jwt token
    TOKEN_ALG = 'HS256'
    # TODO: need to change with uuid
    JTI_LEN = 32  # JWT ID
    ACCESS_TOKEN_EXP = 360  # lifetime in seconds
    ACCESS_TOKEN_CLAIMS = ['iat', 'exp', 'sub', 'iss']
    REFRESH_TOKEN_EXP = 2592000  # 2592000 is 1 month
    REFRESH_TOKEN_CLAIMS = ['iat', 'exp', 'iss', 'jti', 'sub']
