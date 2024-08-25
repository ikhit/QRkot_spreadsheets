from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db import get_async_session
from app.core.user import current_user
from app.crud.charity_project import charity_project_crud
from app.crud.donation import donation_crud
from app.models.user import User
from app.schemas.donation import DonationByUser, DonationCreate, DonationDB
from app.services.utils import distribution_of_donations

router = APIRouter()


@router.post(
    "/", response_model=DonationByUser, response_model_exclude_none=True
)
async def make_donation(
    new_donation: DonationCreate,
    user: User = Depends(current_user),
    session: AsyncSession = Depends(get_async_session),
):
    """
    Сделать пожертвование.
    Доступно только зарегистрированным пользователям.
    """
    sources = await charity_project_crud.get_not_fully_invested(session)
    if sources:
        new_donation = await donation_crud.create(
            new_donation, session, user, distribution=True
        )
        distributed_investments = await distribution_of_donations(
            new_donation, sources
        )
        for investment in distributed_investments:
            session.add(investment)
            await session.commit()
            await session.refresh(investment)
    else:
        new_donation = await donation_crud.create(new_donation, session, user)
    return new_donation


@router.get(
    "/", response_model=list[DonationDB], response_model_exclude_none=True
)
async def get_all_donations(
    session: AsyncSession = Depends(get_async_session),
):
    """
    Вернуть список всех сделанных пожертвований.
    Доступно всем пользователям.
    """
    return await donation_crud.get_multi(session)


@router.get(
    "/my",
    response_model=list[DonationByUser],
    response_model_exclude_none=True,
)
async def get_all_donations_by_current_user(
    user: User = Depends(current_user),
    session: AsyncSession = Depends(get_async_session),
):
    """
    Вернуть список пожертвованний сделанных текущим пользовователем.
    Доступно только зарегистрированным пользователям.
    """
    return await donation_crud.get_by_user(user, session)
