from aiohttp.web import (
    View,
    Response,
) 


class UsersHandler(View):
    async def get(self):
        return Response(text='users get')
    
    async def patch(self):
        return Response(text='users patch')
    
    async def delete(self):
        return Response(text='users delete')


class MonitorHandler(View):
    async def get(self):
        return Response(text='monitor get')


class NotificationsHandler(View):
    async def get(self):
        return Response(text='notifications get')
    
    async def post(self):
        return Response(text='notifications post')
    
    async def patch(self):
        return Response(text='notifications patch')
    
    async def delete(self):
        return Response(text='notifacations delete')
