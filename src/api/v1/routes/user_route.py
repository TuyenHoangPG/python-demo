from api.v1.controllers.user_controller import UserController
from flask import Blueprint, request
from api.v1.middlewares import token_require, valid_roles
from shared.constants import roles
from shared.utils.response import error_not_found, forbidden, success

user_route = Blueprint("users", __name__, url_prefix="/users")
user_controller = UserController()


@user_route.route("/", methods=["GET"])
@token_require
@valid_roles([roles.ADMIN])
def get_list_user(**kwargs):
    args = request.args
    page = int(args.get("page", 1))
    item_per_page = int(args.get("itemPerPage", 5))
    total, items = user_controller.get_list(page, item_per_page)

    return success({"total": total, "items": items})


@user_route.route("/<id>", methods=["PUT"])
@token_require
@valid_roles([roles.ADMIN, roles.USER])
def update_user(id, **kwargs):
    user = kwargs.get("user")
    json_data = request.json
    data_update = {
        "id": id,
        "first_name": json_data.get("first_name"),
        "last_name": json_data.get("last_name"),
        "password": json_data.get("password"),
    }

    try:
        is_updated = user_controller.update(user, data_update)
    except PermissionError as e:
        return forbidden(str(e))

    return success({"is_updated": is_updated})
