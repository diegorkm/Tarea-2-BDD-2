"""Database models for the library management system."""

from dataclasses import dataclass
from datetime import date, datetime

from advanced_alchemy.base import BigIntAuditBase
from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship


class User(BigIntAuditBase):
    """User model with audit fields."""

    __tablename__ = "users"

    username: Mapped[str] = mapped_column(unique=True)
    fullname: Mapped[str]
    password: Mapped[str]

    loans: Mapped[list["Loan"]] = relationship(back_populates="user")
    reviews: Mapped[list["Review"]] = relationship(back_populates="user")

    email: Mapped[str] = mapped_column(unique=True)
    phone: Mapped[str | None]
    address: Mapped[str | None]
    is_active: Mapped[bool] = mapped_column(default=True)



class Book(BigIntAuditBase):
    """Book model with audit fields."""

    __tablename__ = "books"

    title: Mapped[str] = mapped_column(unique=True)
    author: Mapped[str]
    isbn: Mapped[str] = mapped_column(unique=True)
    pages: Mapped[int]
    published_year: Mapped[int]

    loans: Mapped[list["Loan"]] = relationship(back_populates="book")
    categories: Mapped[list["BookCategory"]] = relationship(back_populates="book")
    reviews: Mapped[list["Review"]] = relationship(back_populates="book")

    stock: Mapped[int] = mapped_column(default=1)
    description: Mapped[str | None]
    language: Mapped[str]
    publisher: Mapped[str | None]



class Loan(BigIntAuditBase):
    """Loan model with audit fields."""

    __tablename__ = "loans"

    loan_dt: Mapped[date] = mapped_column(default=datetime.today)
    return_dt: Mapped[date | None]
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    book_id: Mapped[int] = mapped_column(ForeignKey("books.id"))

    user: Mapped[User] = relationship(back_populates="loans")
    book: Mapped[Book] = relationship(back_populates="loans")


class Category(BigIntAuditBase):
    """Category model with audit fields."""

    __tablename__ = "categories"

    name: Mapped[str] = mapped_column(unique=True)
    description: Mapped[str | None]

    books: Mapped[list["BookCategory"]] = relationship(back_populates="category")


class BookCategory(BigIntAuditBase):
    """Association table between books and categories."""

    __tablename__ = "book_categories"

    book_id: Mapped[int] = mapped_column(ForeignKey("books.id"))
    category_id: Mapped[int] = mapped_column(ForeignKey("categories.id"))

    book: Mapped["Book"] = relationship(back_populates="categories")
    category: Mapped["Category"] = relationship(back_populates="books")


class Review(BigIntAuditBase):
    """Review model with audit fields."""

    __tablename__ = "reviews"

    rating: Mapped[int]
    comment: Mapped[str]
    review_date: Mapped[date]
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    book_id: Mapped[int] = mapped_column(ForeignKey("books.id"))

    user: Mapped["User"] = relationship(back_populates="reviews")
    book: Mapped["Book"] = relationship(back_populates="reviews")


@dataclass
class PasswordUpdate:
    """Password update request."""

    current_password: str
    new_password: str


@dataclass
class BookStats:
    """Book statistics data."""

    total_books: int
    average_pages: float
    oldest_publication_year: int | None
    newest_publication_year: int | None
