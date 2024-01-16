from psycopg_pool import AsyncConnectionPool
from aiohttp.web import (
    Application,
    AppKey,
)

from virtual_school_backend.config import Config

CONFIG = AppKey('config', Config)
PG_POOL = AppKey('pg_pool', AsyncConnectionPool)