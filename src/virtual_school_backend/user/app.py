from virtual_school_backend import SubApp
from .handlers import (
    UsersHandler,
    MonitorHandler,
    NotificationsHandler,
)
 

class UserApp(SubApp):
    UrlHandlers = [
        ('/users', UsersHandler),
        ('/monitor', MonitorHandler),
        ('/Notifications', NotificationsHandler),
    ]
