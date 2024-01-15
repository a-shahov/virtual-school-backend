from virtual_school_backend.subapp import SubApp
from virtual_school_backend.validators import validate_json_request
from virtual_school_backend.setup_logging import (
    setup_logging,
    WebDebugFilter,
)
from virtual_school_backend.middlewares import (
    set_permission,
    auth_middleware,
    error_middleware,
)
from virtual_school_backend.appkeys import (
    ROOT_APP,
    CONFIG,
    PG_POOL,
)