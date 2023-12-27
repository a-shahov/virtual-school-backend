from virtual_school_backend import SubApp
from .handlers import (
    LoginHandler,
    RegistrationHandler,
    RefreshHandler,
    LogoutHandler,
)


class AuthApp(SubApp):
    UrlHandlers = [
        ('/login', LoginHandler),
        ('/registration', RegistrationHandler),
        ('/refresh', RefreshHandler),
        ('/logout', LogoutHandler),
    ]
