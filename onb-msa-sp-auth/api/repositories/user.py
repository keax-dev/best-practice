# Tema: consultar los dos usuarios definidos en código.
from api.models.user import User


class UserRepository:
    def __init__(self, users: tuple[User, ...]) -> None:
        self._users = {user.username: user for user in users}

    def find(self, username: str) -> User | None:
        return self._users.get(username)
