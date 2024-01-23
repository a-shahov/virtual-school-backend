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


@pytest.fixture()
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

    return await aiohttp_client(app, server_kwargs={'access_log_format': app[CONFIG].ACCESS_LOG_FMT})

@pytest.fixture()
def reg_data():
    data = {
        'email': 'andrey@yandex.ru',
        'password': '1234qwertyQW',
        'name': 'Андрей',
        'secondname': 'Шахов',
        'patronymic': 'Владимирович',
        'birthdate': '2000-11-22',
        'phone': '8999992233',
        'class': 1,
    }
    return data