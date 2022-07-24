class UserDto:
    def __init__(self, id: str, email, first_name, last_name):
        self.id = id
        self.email = email
        self.first_name = first_name
        self.last_name = last_name

    def to_dict(self):
        return {
            "id": self.id,
            "email": self.email,
            "first_name": self.first_name,
            "last_name": self.last_name,
        }


class UserLoginDto(UserDto):
    def __init__(self, id, email, first_name, last_name, token):
        super().__init__(id, email, first_name, last_name)
        self.token = token

    def to_dict(self):
        return {
            "id": self.id,
            "email": self.email,
            "token": self.token,
            "first_name": self.first_name,
            "last_name": self.last_name,
        }
