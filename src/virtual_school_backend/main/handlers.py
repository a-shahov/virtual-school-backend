from aiohttp.web import View
from aiohttp.web import Response


class InfoHandler(View):
    async def get(self):
        return Response(text='info get')
    
    async def put(self):
        return Response(text='info put')


class NewsHandler(View):
    async def get(self):
        return Response(text='news get')
    
    async def post(self):
        return Response(text='news post')
    
    async def patch(self):
        return Response(text='news patch')
    
    async def delete(self):
        return Response(text='news delete')


class CoursesHandler(View):
    async def get(self):
        return Response(text='courses get')

    async def post(self):
        return Response(text='courses post')

    async def patch(tself):
        return Response(text='courses patch')

    async def delete(self):
        return Response(text='courses delete')
    