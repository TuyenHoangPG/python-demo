from uuid import uuid4

from sqlalchemy import and_
from api.v1.models.user_model import User
from api import db


class UserService:
    def get_by_email(self, email: str):
        return User.query.filter_by(email=email).first()

    def get_by_id(self, id: str):
        return User.query.filter_by(id=id).first()

    def is_user_active(self, id: str):
        user = User.query.filter(and_(User.id == id, User.is_active == True))
        return user is not None

    def update(self, user, data_update: dict):
        user.first_name = data_update.get("first_name")
        user.last_name = data_update.get("last_name")
        if data_update.get("password"):
            user.password = data_update.get("password")
        db.session.commit()
        return True

    def add(self, user_data: dict):
        user = User()
        user.id = str(uuid4())
        user.email = user_data.get("email")
        user.first_name = user_data.get("first_name")
        user.last_name = user_data.get("last_name")
        user.password = user_data.get("password")

        db.session.add(user)
        db.session.commit()

        return user

    def get_list(self, page, item_per_page):
        return User.query.order_by(User.created_at.desc()).paginate(page, item_per_page)

    def get_all_user(self):
        return User.query.filter_by(role="user").all()
