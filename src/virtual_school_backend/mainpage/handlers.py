from aiohttp.web import (
    View,
    Response,
) 

from virtual_school_backend import (
    ROOT_APP,
    CONFIG,
    PG_POOL,
)


class InfoHandler(View):
    async def get(self):
        async with self.request.app[ROOT_APP][PG_POOL].connection() as conn:
            async with conn.cursor() as acur:
                await acur.execute('SELECT * FROM login;')
                print(await acur.fetchone())

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
    