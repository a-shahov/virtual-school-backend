import logging
import asyncio
import sys

import uvloop
from aiohttp.web import Application
from aiohttp.web import run_app

from virtual_school_backend.auth import AuthApp
from virtual_school_backend.user import UserApp
from virtual_school_backend.main import MainApp


class Backend:
    UrlHandlers = []

    def __init__(
        self,
        *,
        port = None,
        host = '127.0.0.1',
    ):
        self._host = host
        self._port = port

    def run(self):
        #  TODO: add logging
        #  TODO: add error handling
        asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())
        app = Application()

        app.add_subapp('/auth', AuthApp().get_app())
        #app.add_subapp('/user', UserApp().get_app())
        #app.add_subapp('/main', MainApp().get_app())

        run_app(app, host=self._host, port=self._port)


def main():
    # TODO: add argparse
    Backend(port=8000).run()


if __name__ == '__main__':
    main()