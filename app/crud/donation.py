from typing import Optional

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.base import CRUDBase
from app.models.donation import Donation
from app.models.user import User


class CRUDDonation(CRUDBase):
    """Класс для реализации CRUD модели пожертвований."""

    async def get_by_user(
        self,
        user: User,
        session: AsyncSession,
    ) -> list[Optional[Donation]]:
        """Вернуть из БД список всехпожертвований сделанных пользователем."""
        donations = await session.execute(
            select(Donation).where(Donation.user_id == user.id)
        )
        return donations.scalars().all()


donation_crud = CRUDDonation(Donation)
