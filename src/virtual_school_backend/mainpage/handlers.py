import logging

from aiohttp.web import (
    View,
    Response,
) 

from virtual_school_backend import set_permission


log = logging.getLogger('aiohttp.web')


class InfoHandler(View):
    @set_permission(['admin'])
    async def get(self):
        return Response(text='info get')
    
    async def put(self):
        return Response(text='info put')


class DocumentsHandler(View):
    '''View for /main/documents'''
    async def post(self):
        reader = await self.request.multipart()
        field = await reader.next()
        log.info('dir field %s', dir(field))
        log.info('field.name %s', field.name)
        log.info('field %s', await field.read())

        return Response()
        


class NewsHandler(View):
    @set_permission(['user'])
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
    