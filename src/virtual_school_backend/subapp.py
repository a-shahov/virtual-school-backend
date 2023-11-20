from aiohttp.web import Application


class SubApp(Application):
    UrlHandlers = []

    def __init__(self, *args, **kwargs):
        Application.__init__(self, *args, **kwargs)

        self._add_views()
    
    def _add_views(self):
        for url, handler in self.UrlHandlers:
            self.router.add_view(url, handler)
