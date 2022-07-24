from functools import wraps

from api.v1.services.auth_service import AuthService
from api.v1.services.user_service import UserService
from flask import request
from jsonschema import validate
from jsonschema.exceptions import ValidationError
from shared.utils.response import (
    error_bad_request,
    forbidden,
    unauthorized,
    error_server_error,
)


def valid_scheme(schema):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            json_data = request.get_json()
            try:
                validate(json_data, schema)
            except ValidationError as error:
                return error_bad_request(error.message)
            except Exception as error:
                return error_bad_request()

            return func(data=json_data, *args, **kwargs)

        return wrapper

    return decorator


def token_require(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            if "Authorization" in request.headers:
                author = request.headers.get("Authorization", "")
                type = author.split(" ")[0]
                token = author.split(" ")[1]

                auth_service = AuthService()
                if not type or not token or type != "Bearer":
                    raise ValueError("Invalid Type")

                payload, is_invalid = auth_service.decode_access_token(token)
                if is_invalid:
                    raise ValueError("Invalid Token")

                user_service = UserService()
                user = user_service.get_by_id(payload.get("user_id"))
                if not user or not user.is_active:
                    raise ValueError("Invalid User")

                return func(user=user, *args, **kwargs)
            else:
                raise ValueError("Token required!")
        except Exception as e:
            print(e)
            return unauthorized("Unauthorized")

    return wrapper


def valid_roles(list_role: list):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            user = kwargs.get("user")

            if not user or not user.role in list_role:
                return forbidden("Forbidden")

            return func(*args, **kwargs)

        return wrapper

    return decorator
