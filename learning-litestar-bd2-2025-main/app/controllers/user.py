"""Controller for User endpoints."""

from typing import Sequence


from advanced_alchemy.exceptions import DuplicateKeyError, NotFoundError
from litestar import Controller, delete, get, patch, post
from litestar.di import Provide
from litestar.dto import DTOData
from litestar.exceptions import HTTPException

from app.controllers import duplicate_error_handler, not_found_error_handler
from app.dtos.user import UserCreateDTO, UserReadDTO, UserUpdateDTO
from app.models import PasswordUpdate, User
from app.repositories.user import UserRepository, provide_user_repo

import re  # ChatGPT me indicó que sirve para el correo
EMAIL_REGEX = re.compile(r"^[^@]+@[^@]+\.[^@]+$")


class UserController(Controller):
    """Controller for user management operations."""

    path = "/users"
    tags = ["users"]
    return_dto = UserReadDTO
    dependencies = {"users_repo": Provide(provide_user_repo)}
    exception_handlers = {
        NotFoundError: not_found_error_handler,
        DuplicateKeyError: duplicate_error_handler,
    }

    @get("/")
    async def list_users(self, users_repo: UserRepository) -> Sequence[User]:
        """Get all users."""
        return users_repo.list()

    @get("/{id:int}")
    async def get_user(self, id: int, users_repo: UserRepository) -> User:
        """Get a user by ID."""
        return users_repo.get(id)

    @post("/", dto=UserCreateDTO)
    async def create_user(
        self,
        data: DTOData[User],
        users_repo: UserRepository,
    ) -> User:
        """Create a new user."""

        user_data = data.as_builtins()

        # Validar formato de email
        email = user_data.get("email")
        if email is None or not EMAIL_REGEX.match(email):
            raise HTTPException(
                status_code=400,
                detail="El email no tiene un formato válido",
            )

        return users_repo.add_with_hashed_password(data)

    @patch("/{id:int}", dto=UserUpdateDTO)
    async def update_user(
        self,
        id: int,
        data: DTOData[User],
        users_repo: UserRepository,
    ) -> User:
        """Update a user by ID."""

        update_data = data.as_builtins()

        # Validar formato de email si se incluye en el update
        if "email" in update_data and update_data["email"] is not None:
            if not EMAIL_REGEX.match(update_data["email"]):
                raise HTTPException(
                    status_code=400,
                    detail="El email no tiene un formato válido",
                )

        user, _ = users_repo.get_and_update(
            match_fields="id",
            id=id,
            **update_data,
        )

        return user

    @post("/{id:int}/update-password", status_code=204)
    async def update_password(
        self,
        id: int,
        data: PasswordUpdate,
        users_repo: UserRepository,
    ) -> None:
        """Update a user's password."""
        user = users_repo.get(id)

        if user.password != data.current_password:
            raise HTTPException(
                detail="Contraseña incorrecta",
                status_code=401,
            )

        user.password = data.new_password
        users_repo.update(user)

    @delete("/{id:int}")
    async def delete_user(self, id: int, users_repo: UserRepository) -> None:
        """Delete a user by ID."""
        users_repo.delete(id)
