from typing import Optional, Union

from fastapi.encoders import jsonable_encoder
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import CharityProject, Donation, User
from app.schemas.charity_project import (
    CharityProjectCreate,
    CharityProjectUpdate,
)
from app.schemas.donation import DonationCreate


class CRUDBase:
    """Базовый класс для реализации CRUD."""

    def __init__(self, model):
        self.model = model

    async def get(
        self,
        obj_id: int,
        session: AsyncSession,
    ) -> Union[CharityProject, Donation]:
        """Получить объект модели по ее id."""
        db_obj = await session.execute(
            select(self.model).where(self.model.id == obj_id)
        )
        return db_obj.scalars().first()

    async def get_multi(
        self, session: AsyncSession
    ) -> Union[list[CharityProject], list[Donation]]:
        """Получить список всех объектов модели из БД."""
        db_objs = await session.execute(select(self.model))
        return db_objs.scalars().all()

    async def create(
        self,
        obj_in: Union[CharityProjectCreate, DonationCreate],
        session: AsyncSession,
        user: Optional[User] = None,
        distribution: Optional[bool] = False,
    ) -> Union[CharityProject, Donation]:
        """
        Создать объект модели. Если нераспределенные средства в фонде
        отсутствуют, внести объект в БД.
        """
        obj_in_data = obj_in.dict()
        if user:
            obj_in_data["user_id"] = user.id
        db_obj = self.model(**obj_in_data)
        if not distribution:
            session.add(db_obj)
            await session.commit()
            await session.refresh(db_obj)
        return db_obj

    async def update(
        self, db_obj, obj_in: CharityProjectUpdate, session: AsyncSession
    ) -> CharityProject:
        """Внести изменения в объект модели в БД."""
        obj_data = jsonable_encoder(db_obj)
        update_data = obj_in.dict(exclude_unset=True)
        for field in obj_data:
            if field in update_data:
                setattr(db_obj, field, update_data[field])
        session.add(db_obj)
        await session.commit()
        await session.refresh(db_obj)
        return db_obj

    async def remove(self, db_obj, session: AsyncSession) -> CharityProject:
        """Удалить объект модели из БД."""
        await session.delete(db_obj)
        await session.commit()
        return db_obj

    async def get_not_fully_invested(
        self, session: AsyncSession
    ) -> list[Union[CharityProject, Donation]]:
        """
        Получить список открытых объектов модели
        (fully_invested = False) из БД.
        """
        not_fully_invested_obj = await session.execute(
            select(self.model)
            .where(~self.model.fully_invested)
            .order_by(self.model.id)
        )
        return not_fully_invested_obj.scalars().all()
