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

from virtual_school_backend import (
    auth_middleware,
    error_middleware,
    ROOT_APP,
    CONFIG,
    PG_POOL,
)
from virtual_school_backend.auth import AuthApp
from virtual_school_backend.user import UserApp
from virtual_school_backend.mainpage import MainApp
from virtual_school_backend.config import Config


class Backend:
    """
    argparse
    background jobs
    setup logging
    unix socket with aiohttp? for faster work?
    pytest
    """
    #  TODO: add logging
    #  TODO: add error handling
    #  TODO: add runner.cleanup
    def __init__(self, *, config, middlewares, subapps):
        self.app = Application(middlewares=middlewares)
        self._add_subapps(subapps)
        self.app[CONFIG] = config
        self.app.cleanup_ctx.append(self.pg_pool)
    
    def _add_subapps(self, subapps):
        for path, subapp in subapps:
            subapp[ROOT_APP] = self.app
            self.app.add_subapp(path, subapp)
    
    @staticmethod
    async def pg_pool(app):
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
        middlewares=[error_middleware, auth_middleware],
        subapps=[
            ('/auth/', AuthApp().app),
            ('/user/', UserApp().app),
            ('/main/', MainApp().app),
        ],
    ).run()


if __name__ == '__main__':
    main()