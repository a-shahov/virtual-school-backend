import logging
from logging.config import dictConfig


class RejectWebDebugFilter(logging.Filter):
    """Filter for rejecting all DEBUG logs from aiohttp.web on console handler"""
    
    def filter(self, record):
        if record.name == 'aiohttp.web' and record.levelno == logging.DEBUG:
            return False
        return True

class AcceptOnlyWebDebugFilter(logging.Filter):
    """Filter for accepting only DEBUG logs from aiohttp.web on console_web_debug handler"""

    def filter(self, record):
        if record.levelno != logging.DEBUG:
            return False
        return True

def setup_logging(config):
    """This function sets logging optimization and logging config"""
    logging._srcfile = None
    logging.logThreads = False
    logging.logProcesses = False
    logging.logMultiprocessing = False
    logging.logAsynctioTasks = False

    dictConfig(config.LOGGING_INFO)
    if config.STARTUP_MODE == 'development':
        dictConfig(config.LOGGING_DEBUG)
