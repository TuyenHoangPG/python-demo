from api.v1.controllers.auth_controller import AuthController
from api.v1.middlewares import valid_scheme
from api.v1.validations.auth_validation import (
    signin_validation_schema,
    signup_validation_schema,
)
from flask import Blueprint
from shared.utils.response import (
    error_bad_request,
    error_not_found,
    success,
    success_created,
    unauthorized,
)

auth_route = Blueprint("auth", __name__, url_prefix="/auth")
auth_controller = AuthController()


@auth_route.route("/sign-up", methods=["POST"])
@valid_scheme(signup_validation_schema)
def signup(data):
    try:
        user_dto = auth_controller.register_user(data)
    except ValueError as e:
        return error_bad_request(str(e))

    return success_created(user_dto)


@auth_route.route("/sign-in", methods=["POST"])
@valid_scheme(signin_validation_schema)
def signin(data):
    try:
        user_dto = auth_controller.signin_user(data)
    except ValueError as e:
        return unauthorized(str(e))
    # user_advance = update_user_advance_service(user.advance, data)

    # return success({"user": user_advance.dict})

    return success(user_dto)
