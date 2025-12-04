"""Repository for Book."""

from typing import Sequence

from advanced_alchemy.repository import SQLAlchemySyncRepository
from sqlalchemy import select, func
from sqlalchemy.orm import Session

from app.models import Book, BookCategory, Review


class BookRepository(SQLAlchemySyncRepository[Book]):
    model_type = Book

    def get_available_books(self) -> Sequence[Book]:
        "Retornar libros con stock > 0."
        stmt = select(Book).where(Book.stock > 0)
        return self.session.execute(stmt).scalars().all()

    def find_by_category(self, category_id: int) -> Sequence[Book]:
        "Buscar libros que pertenezcan a una categoría dada."
        stmt = (
            select(Book)
            .join(BookCategory, BookCategory.book_id == Book.id)
            .where(BookCategory.category_id == category_id)
        )
        return self.session.execute(stmt).scalars().all()

    def get_most_reviewed_books(self, limit: int = 10) -> Sequence[Book]:
        "Libros ordenados por cantidad de reseñas (desc)."
        stmt = (
            select(Book)
            .outerjoin(Review, Review.book_id == Book.id)
            .group_by(Book.id)
            .order_by(func.count(Review.id).desc())
            .limit(limit)
        )
        return self.session.execute(stmt).scalars().all()

    def update_stock(self, book_id: int, quantity: int) -> Book:
        """""
        Actualizar stock de un libro.
        """""
        book = self.get(book_id)
        current_stock = book.stock or 0
        new_stock = current_stock + quantity

        if new_stock < 0:
            raise ValueError("El stock no puede quedar negativo")

        book.stock = new_stock
        self.session.add(book)

        if self.auto_commit:
            self.session.commit()

        return book

    def search_by_author(self, author_name: str) -> Sequence[Book]:
        "Buscar libros por nombre de autor (búsqueda parcial, ilike)."
        stmt = select(Book).where(Book.author.ilike(f"%{author_name}%"))
        return self.session.execute(stmt).scalars().all()


async def provide_book_repo(db_session: Session) -> BookRepository:
    return BookRepository(session=db_session, auto_commit=True)
