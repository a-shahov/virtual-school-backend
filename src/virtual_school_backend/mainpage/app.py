from virtual_school_backend import SubApp
from .handlers import (
    DocumentsHandler,
    InfoHandler,
    NewsHandler,
    CoursesHandler,
)


class MainApp(SubApp):
    UrlHandlers = [
        ('/info', InfoHandler),
        ('/news', NewsHandler),
        ('/courses', CoursesHandler),
        ('/documents', DocumentsHandler),
    ]
