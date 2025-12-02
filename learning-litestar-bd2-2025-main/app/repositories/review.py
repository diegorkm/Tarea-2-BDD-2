"""Repository for Review."""

from advanced_alchemy.repository import SQLAlchemySyncRepository
from sqlalchemy.orm import Session

from app.models import Review


class ReviewRepository(SQLAlchemySyncRepository[Review]):
    model_type = Review


async def provide_review_repo(db_session: Session) -> ReviewRepository:
    return ReviewRepository(session=db_session, auto_commit=True)
