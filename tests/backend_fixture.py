import asyncio
import pytest
import uvloop

from virtual_school_backend import (
    error_middleware,
    auth_middleware,
    setup_logging,
    CONFIG,
)
from virtual_school_backend.__main__ import Backend
from virtual_school_backend.auth import AuthApp
from virtual_school_backend.user import UserApp
from virtual_school_backend.mainpage import MainApp
from virtual_school_backend.config import Config


# TODO: need to write with AppRunner
@pytest.fixture
async def backend_client(aiohttp_client, postgresql, patch_config):
    setup_logging(Config)
    app = Backend(
        config=Config,
        middlewares=[error_middleware, auth_middleware],
        subapps=[
            ('/auth/', AuthApp().app),
            ('/user/', UserApp().app),
            ('/main/', MainApp().app),
        ],
    ).app

    # Here bug server_kwargs not transmitted into TestServer correctly
    return await aiohttp_client(app, server_kwargs={'access_log_format': app[CONFIG].ACCESS_LOG_FMT})
