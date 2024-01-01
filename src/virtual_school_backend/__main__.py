# TODO: переделать импорты
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


class Backend:
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
    def __init__(self, *, config, middlewares, subapps):
        self.app = Application()
        self.middlewares = middlewares
        self._add_subapps(subapps)
        self.app[CONFIG] = config
        self.app.cleanup_ctx.append(self.pg_pool)
    
    def _add_subapps(self, subapps):
        for path, subapp in subapps:
            subapp[ROOT_APP] = self.app
            self.app.add_subapp(path, subapp)
    
    async def pg_pool(self, app):
        async with AsyncConnectionPool(app[CONFIG].DSN, open=False) as pool:
            app[PG_POOL] = pool
            yield

    def run(self):
        run_app(
            self.app, port=self.app[CONFIG].PORT,
            host=self.app[CONFIG].HOST,    
        )


def main():
    #  TODO: add setup configuration
    #  TODO: add argparse
    asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())
    Backend(
        config=Config,
        middlewares=[auth_middleware],
        subapps=[
            ('/auth/', AuthApp().app),
            ('/user/', UserApp().app),
            ('/main/', MainApp().app),
        ],
    ).run()


if __name__ == '__main__':
    main()