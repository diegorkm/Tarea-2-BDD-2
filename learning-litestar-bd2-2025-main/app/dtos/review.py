"""DTOs for Review."""

from advanced_alchemy.extensions.litestar import SQLAlchemyDTO, SQLAlchemyDTOConfig
from app.models import Review


class ReviewReadDTO(SQLAlchemyDTO[Review]):
    config = SQLAlchemyDTOConfig(
        exclude={"user_id", "book_id", "created_at", "updated_at"},
    )


class ReviewCreateDTO(SQLAlchemyDTO[Review]):
    config = SQLAlchemyDTOConfig(
        exclude={"id", "created_at", "updated_at"},
    )


class ReviewUpdateDTO(SQLAlchemyDTO[Review]):
    config = SQLAlchemyDTOConfig(
        exclude={"id", "created_at", "updated_at"},
        partial=True,
    )
