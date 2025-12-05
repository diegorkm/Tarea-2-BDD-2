"""Controller for Book endpoints."""

from typing import Annotated, Sequence

from advanced_alchemy.exceptions import DuplicateKeyError, NotFoundError
from advanced_alchemy.filters import LimitOffset
from litestar import Controller, delete, get, patch, post
from litestar.di import Provide
from litestar.dto import DTOData
from litestar.exceptions import HTTPException
from litestar.params import Parameter

from app.controllers import duplicate_error_handler, not_found_error_handler
from app.dtos.book import BookCreateDTO, BookReadDTO, BookUpdateDTO
from app.models import Book, BookStats, BookCategory
from app.repositories.book import BookRepository, provide_book_repo

class BookController(Controller):
    """Controller for book management operations."""

    path = "/books"
    tags = ["books"]
    return_dto = BookReadDTO
    dependencies = {"books_repo": Provide(provide_book_repo)}
    exception_handlers = {
        NotFoundError: not_found_error_handler,
        DuplicateKeyError: duplicate_error_handler,
    }

    @get("/")
    async def list_books(self, books_repo: BookRepository) -> Sequence[Book]:
        """Get all books."""
        return books_repo.list()

    @get("/{id:int}")
    async def get_book(self, id: int, books_repo: BookRepository) -> Book:
        """Get a book by ID."""
        return books_repo.get(id)

    @post("/", dto=BookCreateDTO)
    async def create_book(
        self,
        data: DTOData[Book],
        books_repo: BookRepository,
    ) -> Book:
        """Create a new book."""
        book_data = data.as_builtins()
        category_items = book_data.pop("categories", [])

        # Validar que el año esté entre 1000 y el año actual
        if not (1000 <= book_data["published_year"] <= 2024):
            raise HTTPException(
                detail="El año de publicación debe estar entre 1000 y 2024",
                status_code=400,
            )

        # Validar que el stock sea > 0 (si no viene, usamos el default 1)
        stock = book_data.get("stock", 1)
        if stock <= 0:
            raise HTTPException(
                detail="El stock debe ser mayor que 0",
                status_code=400,
            )

        # Validar que language tenga 2 letras (ISO 639-1)
        language = book_data.get("language")
        if language is None or len(language) != 2:
            raise HTTPException(
                detail="El language debe ser un código ISO 639-1 de 2 letras (ej: 'es', 'en')",
                status_code=400,
            )

        # Crear el libro
        book = books_repo.add(data.create_instance())

        # Asociar categorías al libro
        for item in category_items:
            books_repo.session.add(
                BookCategory(book_id=book.id, category_id=item["category_id"])
            )

        books_repo.session.commit()

        return book

    @patch("/{id:int}", dto=BookUpdateDTO)
    async def update_book(
        self,
        id: int,
        data: DTOData[Book],
        books_repo: BookRepository,
    ) -> Book:
        """Update a book by ID."""
        update_data = data.as_builtins()

        # Validar que el stock no sea negativo
        if "stock" in update_data and update_data["stock"] is not None:
            if update_data["stock"] < 0:
                raise HTTPException(
                    detail="El stock no puede ser negativo",
                    status_code=400,
                )

        # Validar que language tenga 2 letras
        if "language" in update_data and update_data["language"] is not None:
            if len(update_data["language"]) != 2:
                raise HTTPException(
                    detail="El language debe ser un código ISO 639-1 de 2 letras (ej: 'es', 'en')",
                    status_code=400,
                )

        book, _ = books_repo.get_and_update(
            match_fields="id",
            id=id,
            **update_data,
        )

        return book

    @delete("/{id:int}")
    async def delete_book(self, id: int, books_repo: BookRepository) -> None:
        """Delete a book by ID."""
        books_repo.delete(id)

    @get("/search/")
    async def search_book_by_title(
        self,
        title: str,
        books_repo: BookRepository,
    ) -> Sequence[Book]:
        """Search books by title."""
        return books_repo.list(Book.title.ilike(f"%{title}%"))

    @get("/filter")
    async def filter_books_by_year(
        self,
        year_from: Annotated[int, Parameter(query="from")],
        to: int,
        books_repo: BookRepository,
    ) -> Sequence[Book]:
        """Filter books by published year."""
        return books_repo.list(Book.published_year.between(year_from, to))

    @get("/recent")
    async def get_recent_books(
        self,
        limit: Annotated[int, Parameter(query="limit", default=10, ge=1, le=50)],
        books_repo: BookRepository,
    ) -> Sequence[Book]:
        """Get most recent books."""
        return books_repo.list(
            LimitOffset(offset=0, limit=limit),
            order_by=Book.created_at.desc(),
        )

    @get("/stats")
    async def get_book_stats(
        self,
        books_repo: BookRepository,
    ) -> BookStats:
        """Get statistics about books."""
        total_books = books_repo.count()
        if total_books == 0:
            return BookStats(
                total_books=0,
                average_pages=0,
                oldest_publication_year=None,
                newest_publication_year=None,
            )

        books = books_repo.list()

        average_pages = sum(book.pages for book in books) / total_books
        oldest_year = min(book.published_year for book in books)
        newest_year = max(book.published_year for book in books)

        return BookStats(
            total_books=total_books,
            average_pages=average_pages,
            oldest_publication_year=oldest_year,
            newest_publication_year=newest_year,
        )


    @get("/available")
    async def get_available_books(
        self,
        books_repo: BookRepository,
    ) -> Sequence[Book]:
        """Retornar libros con stock > 0."""
        return books_repo.get_available_books()

    @get("/by-category/{category_id:int}")
    async def get_books_by_category(
        self,
        category_id: int,
        books_repo: BookRepository,
    ) -> Sequence[Book]:
        """Buscar libros de una categoría específica."""
        return books_repo.find_by_category(category_id)

    @get("/most-reviewed")
    async def get_most_reviewed_books(
        self,
        books_repo: BookRepository,
        limit: Annotated[int, Parameter(query="limit", default=10, ge=1)],
    ) -> Sequence[Book]:
        """Libros ordenados por cantidad de reseñas (desc)."""
        return books_repo.get_most_reviewed_books(limit=limit)

    @patch("/{book_id:int}/stock")
    async def update_book_stock(
        self,
        book_id: int,
        quantity: int,
        books_repo: BookRepository,
    ) -> Book:
        """
        Actualizar stock de un libro.
        """
        try:
            return books_repo.update_stock(book_id, quantity)
        except ValueError as exc:
            raise HTTPException(
                status_code=400,
                detail=str(exc),
            )

    @get("/search-by-author")
    async def search_books_by_author(
        self,
        author_name: str,
        books_repo: BookRepository,
    ) -> Sequence[Book]:
        """Buscar libros por nombre de autor (búsqueda parcial, ilike)."""
        return books_repo.search_by_author(author_name)
