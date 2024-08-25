from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.charity_project import charity_project_crud
from app.models.charity_project import CharityProject
from app.schemas.charity_project import CharityProjectUpdate


async def check_charity_project_exists(
    charity_project_id: int, session: AsyncSession
) -> CharityProject:
    """Вернуть благотворительный проект по его id, если он существует."""
    charity_project = await charity_project_crud.get(
        charity_project_id, session
    )
    if not charity_project:
        raise HTTPException(status_code=404, detail="Такого проекта нет!")
    return charity_project


async def check_project_duplicates(
    project_name: str, session: AsyncSession
) -> None:
    """Проверить уникальность названия благотворительного проекта в базе."""
    project_id = await charity_project_crud.get_charity_project_id_by_name(
        project_name, session
    )
    if project_id:
        raise HTTPException(
            status_code=400, detail="Проект с таким именем уже существует!"
        )


async def check_project_fully_invested(
    charity_project: CharityProject,
) -> None:
    """Проверить статус благотворительного проекта."""
    if charity_project.fully_invested:
        raise HTTPException(
            status_code=400,
            detail="Нельзя редактировать или удалять закрытые проекты!",
        )


async def check_project_before_update(
    charity_project_id: int,
    update_data: CharityProjectUpdate,
    session: AsyncSession,
) -> CharityProject:
    """
    Вернуть благотворительный объект после валидации
    новых данных и данных изменяемого благотворительного проекта.
    Изменять можно только существующий проект.
    Новое имя проекта должно быть уникальным,
    а сумма внесенных пожертвований не должна превышать целевую сумму проекта.
    """
    charity_project = await check_charity_project_exists(
        charity_project_id, session
    )
    await check_project_fully_invested(charity_project)
    if update_data.name:
        await check_project_duplicates(update_data.name, session)
    if (
        update_data.full_amount and
        update_data.full_amount < charity_project.invested_amount
    ):
        raise HTTPException(
            status_code=400,
            detail="Сумма сбора должна быть больше, чем сумма, "
            "которую уже инвестировали в проект!",
        )
    return charity_project


async def check_project_before_delete(
    charity_project_id: int, session: AsyncSession
) -> CharityProject:
    """
    Вернуть благотворительный проект если он подходит для удаления.
    Удалять можно только существующий проект,
    на счету которого нет пожертвований.
    """
    charity_project = await check_charity_project_exists(
        charity_project_id, session
    )
    await check_project_fully_invested(charity_project)
    if charity_project.invested_amount:
        raise HTTPException(
            status_code=400,
            detail="Нельзя удалить проект, на который уже внесены средства!",
        )
    return charity_project
