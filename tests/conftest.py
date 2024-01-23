import pytest
import uvloop


pytest_plugins = ('tests.postgresql_fixture', 'tests.backend_fixture')


@pytest.fixture(scope='session')
def event_loop_policy():
    return uvloop.EventLoopPolicy()
