from virtual_school_backend.subapp import SubApp
from virtual_school_backend.validators import validate_json_request
from virtual_school_backend.middlewares import set_permission
from virtual_school_backend.appkeys import (
    ROOT_APP,
    CONFIG,
    PG_POOL,
)