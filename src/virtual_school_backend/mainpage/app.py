from virtual_school_backend import SubApp
from .handlers import InfoHandler
from .handlers import NewsHandler
from .handlers import CoursesHandler


class MainApp(SubApp):
    UrlHandlers = [
        ('/info', InfoHandler),
        ('/news', NewsHandler),
        ('/courses', CoursesHandler),
    ]
