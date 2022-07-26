"""
    Emulate the function of sending notifications
"""
from flask import current_app
from api.v1.services.user_service import UserService
import time


def send_notification(user_id: str):
    with current_app.app_context():
        user_service = UserService()
        users = user_service.get_all_user()
        users = [user for user in users if user.id != user_id]

        for user in users:
            print(user.id)
            time.sleep(1)

        return len(users)
