from flask import Blueprint
from api.v1.routes.user_route import user_route
from api.v1.routes.auth_route import auth_route
from api.v1.routes.post_route import post_route


api_v1 = Blueprint("api_v1", __name__, url_prefix="/api/v1")
api_v1.register_blueprint(user_route)
api_v1.register_blueprint(auth_route)
api_v1.register_blueprint(post_route)
