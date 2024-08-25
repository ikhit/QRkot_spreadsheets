from typing import Optional

from pydantic import Extra, Field, PositiveInt

from app.core.config import settings
from app.schemas.base import SchemaBase, SchemaDB


class CharityProjectBase(SchemaBase):
    """Базовый класс pydantic модели CharityProject."""

    name: Optional[str] = Field(
        None,
        max_length=settings.MAX_CHARITY_PROJECT_NAME_LEN,
    )
    description: Optional[str]

    class Config:
        extra = Extra.forbid
        min_anystr_length = settings.MIN_ANYSTR_LEN


class CharityProjectDB(CharityProjectBase, SchemaDB):
    """
    Класс-схема для вывода полной информации о
    благотворительном проекте из БД.
    """

    pass


class CharityProjectUpdate(CharityProjectBase):
    """Класс-схема для редактирования благотворительного проекта."""

    class Config:
        schema_extra = {
            "example": {
                "name": settings.CHARITY_PROJECT_NAME_EXAMPLE,
                "description": settings.CHARITY_PROJECT_DESCRIPTION_EXAMPLE,
                "full_amount": settings.CHARITY_PROJECT_FULL_AMOUNT_EXAMPLE,
            }
        }


class CharityProjectCreate(CharityProjectUpdate):
    """Класс-схема для создания благотворительного проекта."""

    name: str = Field(
        ...,
        max_length=settings.MAX_CHARITY_PROJECT_NAME_LEN,
    )
    description: str
    full_amount: PositiveInt
    invested_amount: PositiveInt = Field(0)
