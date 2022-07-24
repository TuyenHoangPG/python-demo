from api.v1.dtos.user_dto import UserDto, UserLoginDto
from api.v1.services.auth_service import AuthService
from api.v1.services.user_service import UserService


class AuthController:
    user_service = UserService()
    auth_service = AuthService()

    def register_user(self, data: dict):
        email = data.get("email")
        user = self.user_service.get_by_email(email)

        if user:
            raise ValueError("This email is already exist!")

        user = self.user_service.add(data)
        user_dto = UserDto(
            id=user.id,
            email=user.email,
            first_name=user.first_name,
            last_name=user.last_name,
        )

        return user_dto.to_dict()

    def signin_user(self, data: dict):
        email = data.get("email")
        password = data.get("password")

        user = self.user_service.get_by_email(email)

        if not user:
            raise ValueError("Incorrect email or password!")

        if not user.check_password(password):
            raise ValueError("Incorrect email or password!")

        token = self.auth_service.generate_access_token(user.id)
        user_dto = UserLoginDto(
            id=user.id,
            email=user.email,
            first_name=user.first_name,
            last_name=user.last_name,
            token=token,
        )

        return user_dto.to_dict()
