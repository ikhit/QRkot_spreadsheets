from typing import Optional, Union

from sqlalchemy import select
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
    ) -> Union[None, list[tuple[str]]]:
        closed_projects = await session.execute(
            select(CharityProject).where(CharityProject.fully_invested)
        )
        closed_projects = closed_projects.scalars().all()
        complection_rate_list = []
        for project in closed_projects:
            time_delta = project.close_date - project.create_date
            complection_rate_list.append((project.name, str(time_delta), project.description))
        return complection_rate_list


charity_project_crud = CRUDCharityProject(CharityProject)
