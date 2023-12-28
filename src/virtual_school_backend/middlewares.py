from aiohttp.web import middleware


@middleware
async def error_middleware(request, handler):
    pass

@middleware
async def auth_middleware(request, handler):
    resp = await handler(request)
    return resp