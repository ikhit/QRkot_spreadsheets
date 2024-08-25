from datetime import datetime

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.validators import (
    check_project_before_delete,
    check_project_before_update,
    check_project_duplicates,
)
from app.core.db import get_async_session
from app.core.user import current_superuser
from app.crud.charity_project import charity_project_crud
from app.crud.donation import donation_crud
from app.schemas.charity_project import (
    CharityProjectCreate,
    CharityProjectDB,
    CharityProjectUpdate,
)
from app.services.utils import distribution_of_donations

router = APIRouter()


@router.get(
    "/",
    response_model=list[CharityProjectDB],
    response_model_exclude_none=True,
)
async def get_all_charity_projects(
    session: AsyncSession = Depends(get_async_session),
):
    """
    Получить список всех благотворительных проектов.
    Доступно всем пользователям.
    """
    return await charity_project_crud.get_multi(session)


@router.delete(
    "/{charity_project_id}",
    response_model=CharityProjectDB,
    response_model_exclude_none=True,
    dependencies=[Depends(current_superuser)],
)
async def delete_charity_project(
    charity_project_id: int, session: AsyncSession = Depends(get_async_session)
):
    """
    Удалить благотворительный проект. Доступно только для суперпользователя.
    Нельзя удалить проект, если в него вложены пожертвования.
    """
    charity_project = await check_project_before_delete(
        charity_project_id, session
    )
    return await charity_project_crud.remove(charity_project, session)


@router.post(
    "/",
    response_model=CharityProjectDB,
    response_model_exclude_none=True,
    dependencies=[Depends(current_superuser)],
)
async def create_charity_project(
    charity_project: CharityProjectCreate,
    session: AsyncSession = Depends(get_async_session),
):
    """
    Создать благотворительный проект.
    Доступно только для суперпользователя.
    """
    await check_project_duplicates(charity_project.name, session)
    sources = await donation_crud.get_not_fully_invested(session)
    if sources:
        charity_project = await charity_project_crud.create(
            charity_project, session, distribution=True
        )
        distributed_investments = await distribution_of_donations(
            charity_project, sources
        )
        for investment in distributed_investments:
            session.add(investment)
            await session.commit()
            await session.refresh(investment)
    else:
        charity_project = await charity_project_crud.create(
            charity_project, session
        )
    return charity_project


@router.patch(
    "/{charity_project_id}",
    response_model=CharityProjectDB,
    response_model_exclude_none=True,
    dependencies=[Depends(current_superuser)],
)
async def partially_update_charity_project(
    charity_project_id: int,
    update_data: CharityProjectUpdate,
    session: AsyncSession = Depends(get_async_session),
):
    """
    Внести изменения в благотворительный проект.
    Доступно только для суперпользователя.
    Изменять можно только description, full_amount, name.
    """
    charity_project = await check_project_before_update(
        charity_project_id, update_data, session
    )
    if (
        update_data.full_amount and
        update_data.full_amount == charity_project.invested_amount
    ):
        charity_project.fully_invested = True
        charity_project.close_date = datetime.now()
    return await charity_project_crud.update(
        charity_project, update_data, session
    )
