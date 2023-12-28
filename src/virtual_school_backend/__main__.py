import logging
import asyncio
import sys

import uvloop
from psycopg_pool import AsyncConnectionPool
from aiohttp.web import (
    Application,
    AppRunner,
    TCPSite,
    run_app,
)

from virtual_school_backend.auth import AuthApp
from virtual_school_backend.user import UserApp
from virtual_school_backend.mainpage import MainApp
from virtual_school_backend.config import Config
from virtual_school_backend.middlewares import auth_middleware
from virtual_school_backend.appkeys import (
    ROOT_APP,
    CONFIG,
    PG_POOL,
)


class Backend(Application):
    """
    В миддлваре auth + декораторы на каждый хендлер с доступом
    декораторы хендлеров для валидации запросов
    в мидлваре обработку ошибок?
    argparse
    background jobs
    setup logging
    middlewares
    unix socket with aiohttp? for faster work?
    pytest
    """
    #  TODO: add logging
    #  TODO: add error handling
    #  TODO: add runner.cleanup

    def __init__(self, *args, **kwargs):
        super().__init__(*args, middlewares=[auth_middleware], **kwargs)
        
        self[CONFIG] = Config
        self._add_subapps()
        self.cleanup_ctx.append(self.pg_pool)
    
    def _add_subapps(self):
        subapps = (
            ('/auth/', AuthApp()),
            ('/user/', UserApp()),
            ('/main/', MainApp()),
        )

        for path, subapp in subapps:
            subapp[ROOT_APP] = self
            self.add_subapp(path, subapp)

    async def pg_pool(self, unused):
        async with AsyncConnectionPool(self[CONFIG].DSN, open=False) as pool:
            self[PG_POOL] = pool
            yield


def main():
    #  TODO: add setup configuration
    #  TODO: add argparse
    asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())
    #  TODO: move to config
    run_app(Backend(), port=8000, host='127.0.0.1')


if __name__ == '__main__':
    main()