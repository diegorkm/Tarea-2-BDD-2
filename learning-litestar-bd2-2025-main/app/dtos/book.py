"""Data Transfer Objects for Book endpoints."""

from advanced_alchemy.extensions.litestar import SQLAlchemyDTO, SQLAlchemyDTOConfig

from app.models import Book

#importaciones obtenidas por chatgpt para solucionar errores mios
from typing import Optional, List
from pydantic import BaseModel


class BookReadDTO(SQLAlchemyDTO[Book]):
    """DTO for reading book data."""

    config = SQLAlchemyDTOConfig()


class CategoryInput(BaseModel):
    category_id: int

class BookCreateDTO(SQLAlchemyDTO[Book]):
    config = SQLAlchemyDTOConfig(
        exclude={
            "id",
            "created_at",
            "updated_at",
            "loans",
            "reviews",
            "categories",
        }
    )
    categories: Optional[List[CategoryInput]] = None


class BookUpdateDTO(SQLAlchemyDTO[Book]):
    """DTO for updating books with partial data."""

    config = SQLAlchemyDTOConfig(
        exclude={"id", "created_at", "updated_at", "loans"},
        partial=True,
    )
