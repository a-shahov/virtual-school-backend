from aiohttp.web import Application


class SubApp:
    UrlHandlers = []

    def __init__(self):
        self._app = Application()

        self._add_views()
    
    def _add_views(self):
        for url, handler in self.UrlHandlers:
            self._app.router.add_view(url, handler)
    
    def get_app(self):
        return self._app
