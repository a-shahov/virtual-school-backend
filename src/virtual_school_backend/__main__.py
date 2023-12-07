import logging
import asyncio
import sys

import uvloop
from aiohttp.web import (
    Application,
    AppRunner,
    TCPSite,
    run_app,
)

from virtual_school_backend.auth import AuthApp
from virtual_school_backend.user import UserApp
from virtual_school_backend.mainpage import MainApp


class Backend(Application):
    """
    routing
    config
    argparse
    background jobs
    setup logging
    middlewares
    setup database
    unix socket
    pytest
    """
    #  TODO: add logging
    #  TODO: add error handling
    #  TODO: add runner.cleanup
    def __init__(
        self,
        *args,
        **kwargs,
    ):
        super().__init__(*args, **kwargs)
        
        self.add_subapp('/auth/', AuthApp())
        self.add_subapp('/user/', UserApp())
        self.add_subapp('/main/', MainApp())


def main():
    #  TODO: add argparse
    asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())
    run_app(Backend(), port=8000, host='127.0.0.1')


if __name__ == '__main__':
    main()