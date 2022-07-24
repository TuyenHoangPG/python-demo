from api.v1.controllers.post_controller import PostController
from api.v1.controllers.user_controller import UserController
from api.v1.middlewares import token_require, valid_roles, valid_scheme
from api.v1.validations.post_validation import (
    add_post_validation_schema,
    update_post_validation_schema,
)
from flask import Blueprint, request
from shared.constants import roles
from shared.utils.response import error_not_found, forbidden, success

post_route = Blueprint("posts", __name__, url_prefix="/posts")
post_controller = PostController()


@post_route.route("/", methods=["GET"])
def get_list_post():
    args = request.args
    page = int(args.get("page", 1))
    item_per_page = int(args.get("itemPerPage", 5))
    total, items = post_controller.get_list(page, item_per_page)

    return success({"total": total, "items": items})


@post_route.route("/", methods=["POST"])
@token_require
@valid_scheme(add_post_validation_schema)
def add_new_post(data, **kwargs):
    user = kwargs.get("user")
    data["created_by"] = user.id
    post_dto = post_controller.add(data)

    return success(post_dto)


@post_route.route("/<id>", methods=["PUT"])
@token_require
@valid_scheme(update_post_validation_schema)
def update_post(id, data, **kwargs):
    user = kwargs.get("user")
    data["id"] = id
    try:
        is_updated = post_controller.update(user, data)
    except ValueError as e:
        return error_not_found(str(e))
    except PermissionError as e:
        return forbidden(str(e))

    return success({"is_updated": is_updated})


@post_route.route("/<id>", methods=["DELETE"])
@token_require
def delete_post(id, **kwargs):
    user = kwargs.get("user")
    try:
        is_deleted = post_controller.delete(user, id)
    except ValueError as e:
        return error_not_found(str(e))
    except PermissionError as e:
        return forbidden(str(e))

    return success({"is_deleted": is_deleted})
