"""Controller for Review"""

from typing import Sequence

from litestar import Controller, get, post, patch, delete
from litestar.di import Provide
from litestar.dto import DTOData
from litestar.exceptions import HTTPException

from advanced_alchemy.exceptions import NotFoundError, DuplicateKeyError

from app.controllers import not_found_error_handler, duplicate_error_handler
from app.dtos.review import ReviewReadDTO, ReviewCreateDTO, ReviewUpdateDTO
from app.models import Review
from app.repositories.review import ReviewRepository, provide_review_repo


class ReviewController(Controller):
    path = "/reviews"
    tags = ["reviews"]
    return_dto = ReviewReadDTO
    dependencies = {"reviews_repo": Provide(provide_review_repo)}
    exception_handlers = {
        NotFoundError: not_found_error_handler,
        DuplicateKeyError: duplicate_error_handler,
    }

    @get("/")
    async def list_reviews(self, reviews_repo: ReviewRepository) -> Sequence[Review]:
        return reviews_repo.list()

    @get("/{id:int}")
    async def get_review(self, id: int, reviews_repo: ReviewRepository) -> Review:
        return reviews_repo.get(id)

    @post("/", dto=ReviewCreateDTO)
    async def create_review(
        self,
        data: DTOData[Review],
        reviews_repo: ReviewRepository,
    ) -> Review:

        # Validación rating entre 1 y 5
        rating = data.as_builtins().get("rating")
        if rating < 1 or rating > 5:
            raise HTTPException(status_code=400, detail="rating must be between 1 and 5")

        review = data.create_instance()
        return reviews_repo.add(review)

    @patch("/{id:int}", dto=ReviewUpdateDTO)
    async def update_review(
        self,
        id: int,
        data: DTOData[Review],
        reviews_repo: ReviewRepository,
    ) -> Review:
        review, _ = reviews_repo.get_and_update(
            match_fields="id",
            id=id,
            **data.as_builtins(),
        )
        return review

    @delete("/{id:int}")
    async def delete_review(self, id: int, reviews_repo: ReviewRepository) -> None:
        reviews_repo.delete(id)
