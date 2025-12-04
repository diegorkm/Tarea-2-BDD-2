"""Controller for Loan endpoints."""

from typing import Sequence

from advanced_alchemy.exceptions import DuplicateKeyError, NotFoundError
from litestar import Controller, delete, get, patch, post
from litestar.di import Provide
from litestar.dto import DTOData

from app.controllers import duplicate_error_handler, not_found_error_handler
from app.dtos.loan import LoanCreateDTO, LoanReadDTO, LoanUpdateDTO
from app.models import Loan, LoanStatus
from app.repositories.loan import LoanRepository, provide_loan_repo

from datetime import datetime, timedelta


class LoanController(Controller):
    """Controller for loan management operations."""

    path = "/loans"
    tags = ["loans"]
    return_dto = LoanReadDTO
    dependencies = {"loans_repo": Provide(provide_loan_repo)}
    exception_handlers = {
        NotFoundError: not_found_error_handler,
        DuplicateKeyError: duplicate_error_handler,
    }

    @get("/")
    async def list_loans(self, loans_repo: LoanRepository) -> Sequence[Loan]:
        """Get all loans."""
        return loans_repo.list()

    @get("/{id:int}")
    async def get_loan(self, id: int, loans_repo: LoanRepository) -> Loan:
        """Get a loan by ID."""
        return loans_repo.get(id)

    @post("/", dto=LoanCreateDTO)
    async def create_loan(
        self,
        data: DTOData[Loan],
        loans_repo: LoanRepository,
    ) -> Loan:
        """Create a new loan."""

        loan = data.create_instance()

        # Asegurar loan_dt
        if loan.loan_dt is None:
            loan.loan_dt = datetime.today().date()

        # due_date = loan_dt + 14 días
        loan.due_date = loan.loan_dt + timedelta(days=14)

        # Status por defecto
        loan.status = LoanStatus.ACTIVE

        # fine_amount se deja en None al inicio
        return loans_repo.add(loan)


    @patch("/{id:int}", dto=LoanUpdateDTO)
    async def update_loan(
        self,
        id: int,
        data: DTOData[Loan],
        loans_repo: LoanRepository,
    ) -> Loan:
        """Update a loan by ID."""

        update_data = data.as_builtins()

        # asegurarr que solo venga status
        allowed_keys = {"status"}
        extra_keys = set(update_data.keys()) - allowed_keys
        for key in extra_keys:
            update_data.pop(key, None)

        loan, _ = loans_repo.get_and_update(
            match_fields="id",
            id=id,
            **update_data,
        )
        return loan



    @delete("/{id:int}")
    async def delete_loan(self, id: int, loans_repo: LoanRepository) -> None:
        """Delete a loan by ID."""
        loans_repo.delete(id)
