from datetime import datetime

from sqlalchemy import Boolean, CheckConstraint, Column, DateTime, Integer

from app.core.config import settings as preset
from app.core.db import Base


class CharityProjectDonationBase(Base):
    """
    Абстрактный родительский класс для моделей CharityProject и Donation.
    """

    __abstract__ = True
    full_amount = Column(Integer)
    invested_amount = Column(Integer, default=preset.DEFAULT_INVESTED_AMOUNT)
    fully_invested = Column(Boolean, default=False)
    create_date = Column(DateTime, default=datetime.now)
    close_date = Column(DateTime)
    __table_args__ = (
        CheckConstraint(
            sqltext="full_amount >= 0",
            name="check_full_amount_is_not_negative",
        ),
        CheckConstraint(
            sqltext="invested_amount >= 0",
            name="check_invested_amount_is_not_negative",
        ),
        CheckConstraint(
            sqltext="full_amount >= invested_amount",
            name="check_invested_amount_less_or_equal_to_full_amount",
        ),
    )

    def amount_difference(self):
        """
        Вернуть разницу между необходимой суммой и внесеными пожертвованиями.
        """
        return self.full_amount - self.invested_amount
