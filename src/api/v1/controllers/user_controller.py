from api.v1.dtos.user_dto import UserDto
from api.v1.services.user_service import UserService


class UserController:
    user_service = UserService()

    def get_list(self, page=0, item_per_page=5):
        data = self.user_service.get_list(page, item_per_page)
        total = data.total
        items = data.items
        items = [
            UserDto(
                id=user.id,
                email=user.email,
                first_name=user.first_name,
                last_name=user.last_name,
            ).to_dict()
            for user in items
        ]

        return total, items

    def update(self, user, data_update: dict):
        if user is None or user.id != data_update.get("id"):
            raise PermissionError("Not allow update!")

        return self.user_service.update(user, data_update)
