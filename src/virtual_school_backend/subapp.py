from aiohttp.web import Application


class SubApp:
    UrlHandlers = []
    CleanupCtxs = []
    Middlewares = []

    def __init__(self):
        self.app = Application(middlewares=self.Middlewares)
        self._add_views()
        self._add_cleanup_ctxs()
    
    def _add_cleanup_ctxs(self):
        for cleanup_ctx in self.CleanupCtxs:
            self.app.cleanup_ctx.append(cleanup_ctx)
    
    def _add_views(self):
        for url, handler in self.UrlHandlers:
            self.app.router.add_view(url, handler)
