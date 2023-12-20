from aiohttp.web import middlewares


@middlewares
async def error_middleware(request, handler):
    pass

@middlewares
async def auth_middleware(request, handler):
    pass