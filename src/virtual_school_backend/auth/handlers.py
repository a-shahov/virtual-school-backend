from aiohttp.web import View
from aiohttp.web import Response


class LoginHandler(View):
    async def get(self):
        return Response(text='login')


class RegistrationHandler(View):
    async def get(self):
        return Response(text='registration')


class LogoutHandler(View):
    async def get(self):
        return Response(text='logout')


class WhoamiHandler(View):
    async def get(self):
        return Response(text='whoami')
