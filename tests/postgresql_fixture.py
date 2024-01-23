import pytest
from pytest import MonkeyPatch

from virtual_school_backend.config import Config
from virtual_school_backend.scripts import init_db


@pytest.fixture(scope='session')
def patch_config():
    with MonkeyPatch.context() as mp:
        DSN = 'dbname=test2 user=postgres host=127.0.0.1 port=5432 password=qwerty'
        mp.setattr(Config, 'DSN', DSN)
        mp.setattr(Config, 'STARTUP_MODE', 'DEVELOPMENT')
        yield mp

@pytest.fixture(scope='session')
def postgresql(patch_config):
    init_db()
    yield
