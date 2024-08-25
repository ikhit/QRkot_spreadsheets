from datetime import datetime
from typing import Optional

from pydantic import BaseModel, PositiveInt


class SchemaBase(BaseModel):
    """Базовый класс для pydantic моеделй CharityProject и Donation."""

    full_amount: Optional[PositiveInt]


class SchemaDB(BaseModel):
    """Базовый класс для pydantic моделей CharityProjectDB и DonationDB."""

    id: int
    fully_invested: bool
    invested_amount: int
    create_date: datetime
    close_date: Optional[datetime]

    class Config:
        orm_mode = True
