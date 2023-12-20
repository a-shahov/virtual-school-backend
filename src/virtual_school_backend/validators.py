from functools import wraps
import json

def validate_data(data):
    print(data)
    return json.loads(data)

def validate_json_request(scheme):
    def wrapper(func):
        @wraps(func)
        async def wrapped(self):
            return await func(self, validate_data(await self.request.text()))
        return wrapped
    return wrapper