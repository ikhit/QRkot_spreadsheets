from sqlalchemy import Column, String, Text

from app.core.config import settings
from app.models.base import CharityProjectDonationBase


class CharityProject(CharityProjectDonationBase):
    """Модель благотворительного проекта для БД."""

    name = Column(
        String(settings.MAX_CHARITY_PROJECT_NAME_LEN),
        unique=True,
        nullable=False,
    )
    description = Column(Text, nullable=False)
