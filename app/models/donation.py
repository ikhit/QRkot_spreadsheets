from sqlalchemy import Column, ForeignKey, Integer, Text

from app.models.base import CharityProjectDonationBase


class Donation(CharityProjectDonationBase):
    """Модель пожертвований для БД."""

    comment = Column(Text)
    user_id = Column(Integer, ForeignKey("user.id"))
