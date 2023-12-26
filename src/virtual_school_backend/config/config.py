import os
import tomllib
from pathlib import Path

from dotenv import load_dotenv


# Load .env file in environment
load_dotenv()

# Load static configuration file
with Path(__file__).with_name('config.toml').open('rb') as toml_f:   
    conf_toml = tomllib.load(toml_f)

# Load pyproject.toml
with Path(__file__).parents[3].joinpath('pyproject.toml').open('rb') as toml_f:
    pyproj_toml = tomllib.load(toml_f)


class Config:
    """Class for storing full backend configuration"""
    BACKEND_NAME = pyproj_toml['project']['name']

    DSN = (
        f'dbname={os.getenv("PG_NAME")} '
        f'user={os.getenv("PG_USER")} '
        f'host={os.getenv("PG_HOST")} '
        f'port={os.getenv("PG_PORT")} '
        f'password={os.getenv("PG_PASSWORD")}'
    )

    PASS_KEY = os.getenv('BLAKE2_KEY')  # key for generate password hash (blake2b)
    SALT_LEN = conf_toml['crypt_password']['salt_len']

    TOKEN_KEY = os.getenv('TOKEN_KEY')  # key for generate jwt token
    TOKEN_ALG = conf_toml['jwt_token']['token_algorithm']
    JTI_LEN = conf_toml['jwt_token']['jti_len']
    ACCESS_TOKEN_EXP = conf_toml['jwt_token']['access_token_exp']
    REFRESH_TOKEN_EXP = conf_toml['jwt_token']['refresh_token_exp']
