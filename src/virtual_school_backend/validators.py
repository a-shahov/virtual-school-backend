from functools import wraps
import json
from json import JSONDecodeError

from aiohttp.web import HTTPBadRequest
from jsonschema import (
    Draft202012Validator,
    ValidationError,
)


def validate_data(data, validator):
    try:
        json_data = json.loads(data)
    except JSONDecodeError:
        raise HTTPBadRequest(reason='invalid json data in request')

    validation_errors = []
    for error in validator.iter_errors(json_data):
        # TODO: need add logging!
        # TODO: need to research error.path[0]
        error.reason = f'{error.path[0]} validation error'
        validation_errors.append(error)

    if validation_errors:
        raise ExceptionGroup('Validation errors', validation_errors)

    return json_data

def validate_json_request(schema, format_checker=None):

    Draft202012Validator.check_schema(schema)
    validator = Draft202012Validator(
        schema,
        format_checker=format_checker or Draft202012Validator.FORMAT_CHECKER,
    )

    def wrapper(func):

        @wraps(func)
        async def wrapped(self):
            return await func(self, validate_data(await self.request.text(), validator))
        return wrapped

    return wrapper