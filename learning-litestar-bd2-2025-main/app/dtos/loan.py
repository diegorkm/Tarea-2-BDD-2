"""DTOs for Loan."""

from advanced_alchemy.extensions.litestar import SQLAlchemyDTO, SQLAlchemyDTOConfig

from app.models import Loan


class LoanReadDTO(SQLAlchemyDTO[Loan]):
    # Incluimos due_date, fine_amount y status
    config = SQLAlchemyDTOConfig()


class LoanCreateDTO(SQLAlchemyDTO[Loan]):
    # El cliente no debe mandar due_date, fine_amount ni status
    config = SQLAlchemyDTOConfig(
        exclude={
            "id",
            "created_at",
            "updated_at",
            "due_date",
            "fine_amount",
            "status",
        },
    )


class LoanUpdateDTO(SQLAlchemyDTO[Loan]):
    # Solo permitimos actualizar status
    config = SQLAlchemyDTOConfig(
        include={"status"},
        partial=True,
    )
