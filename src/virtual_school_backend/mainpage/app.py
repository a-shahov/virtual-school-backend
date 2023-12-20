from virtual_school_backend import SubApp
from .handlers import (
    InfoHandler,
    NewsHandler,
    CoursesHandler,
)


class MainApp(SubApp):
    UrlHandlers = [
        ('/info', InfoHandler),
        ('/news', NewsHandler),
        ('/courses', CoursesHandler),
    ]
