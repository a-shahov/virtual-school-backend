from virtual_school_backend import SubApp
from .handlers import LoginHandler
from .handlers import RegistrationHandler
from .handlers import LogoutHandler
from .handlers import WhoamiHandler


class AuthApp(SubApp):
    UrlHandlers = [
        ('/login', LoginHandler),
        ('/registration', RegistrationHandler),
        ('/logout', LogoutHandler),
        ('/whoami', WhoamiHandler),
    ]