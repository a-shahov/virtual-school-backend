from virtual_school_backend import SubApp
from .handlers import (
    LoginHandler,
    RegistrationHandler,
    LogoutHandler,
    WhoamiHandler,
)


class AuthApp(SubApp):
    UrlHandlers = [
        ('/login', LoginHandler),
        ('/registration', RegistrationHandler),
        ('/logout', LogoutHandler),
        ('/whoami', WhoamiHandler),
    ]