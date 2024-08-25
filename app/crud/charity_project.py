from datetime import timedelta
from typing import Optional, Union

from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.base import CRUDBase
from app.models.charity_project import CharityProject


class CRUDCharityProject(CRUDBase):
    """Класс для реализации CRUD модели благотворительного проекта."""

    async def get_charity_project_id_by_name(
        self, charity_project_name: str, session: AsyncSession
    ) -> Optional[int]:
        """Вернуть id благотворительного проекта по его названию."""
        charity_project_id = await session.execute(
            select(CharityProject.id).where(
                CharityProject.name == charity_project_name
            )
        )
        return charity_project_id.scalars().first()

    async def get_projects_by_completion_rate(
        self, session: AsyncSession
    ) -> Union[None, list[tuple[str, timedelta]]]:
        """
        Вернуть список всех закрытых проектов,
        отсортированных по скорости закрытия проекта.
        """
        closed_projects = await session.execute(
            select(
                [
                    CharityProject.name,
                    (
                        func.julianday(CharityProject.close_date) -
                        func.julianday(CharityProject.create_date)
                    ).label("completion_rate"),
                    CharityProject.description,
                ]
            )
            .where(CharityProject.fully_invested)
            .order_by("completion_rate")
        )
        return closed_projects.all()


charity_project_crud = CRUDCharityProject(CharityProject)
