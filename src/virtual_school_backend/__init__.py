__version__ = "0.1.0"

from virtual_school_backend.subapp import SubApp
from virtual_school_backend.validators import validate_json_request
from virtual_school_backend.setup_logging import (
    setup_logging,
    RejectWebDebugFilter,
    AcceptOnlyWebDebugFilter,
)
from virtual_school_backend.middlewares import (
    set_permission,
    auth_middleware,
    error_middleware,
)
from virtual_school_backend.appkeys import (
    CONFIG,
    PG_POOL,
)