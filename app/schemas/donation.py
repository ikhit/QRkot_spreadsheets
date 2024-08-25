from datetime import datetime
from typing import Optional

from pydantic import Field, PositiveInt

from app.core.config import settings
from app.schemas.base import SchemaBase, SchemaDB


class DonationBase(SchemaBase):
    """Базовый класс pydantic модели Donation."""

    comment: Optional[str]


class DonationCreate(DonationBase):
    """Класс-схема для создания пожертвования."""

    full_amount: PositiveInt
    invested_amount: PositiveInt = Field(0)

    class Config:
        schema_extra = {
            "example": {
                "comment": settings.DONATION_COMMENT_EXMAPLE,
                "full_amount": settings.DONATION_FULL_AMOUNT_EXMAPLE,
            }
        }


class DonationDB(DonationBase, SchemaDB):
    """
    Класс-схема для вывода полной информации о
    пожертвовании из БД.
    """

    user_id: int


class DonationByUser(DonationBase):
    """
    Класс-схема для вывода информации о пожертвованиях с
    деланными текущим пользователем.
    """

    id: int
    create_date: datetime

    class Config:
        orm_mode = True
