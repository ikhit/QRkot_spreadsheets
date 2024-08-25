from datetime import datetime
from typing import Union

from app.models.charity_project import CharityProject
from app.models.donation import Donation


async def update_invested_amount(
    obj_to_update: Union[CharityProject, Donation],
    balance_change: int,
) -> Union[CharityProject, Donation]:
    """
    Внести изменения инвестированной суммы объекта.
    Закрыть проект, если инвестируемая сумма равна требуемой.
    Добавить объект в сессию и вернуть измененный объект.
    """
    obj_to_update.invested_amount += balance_change
    if obj_to_update.full_amount == obj_to_update.invested_amount:
        obj_to_update.fully_invested = True
        obj_to_update.close_date = datetime.now()
    return obj_to_update


async def distribution_of_donations(
    target: Union[CharityProject, Donation],
    sources: Union[list[CharityProject], list[Donation]],
) -> list[CharityProject, Donation]:
    """
    Вернуть список объектов благотворительных проектов и пожертсований.
    При создании пожертвования, средства перечисляются на
    первый незакрытый благотворительный проект.
    При создании благотворительного проекта, на его счет зачисляются
    средства, оставшиеся от других пожертвований.
    """
    distributed_investments = []
    while not target.fully_invested and sources:
        source = sources.pop(0)
        balance_amount = source.amount_difference()
        amount_needed = target.amount_difference()
        balance_change = min(balance_amount, amount_needed)
        target = await update_invested_amount(
            target,
            balance_change,
        )
        source = await update_invested_amount(
            source,
            balance_change,
        )
        distributed_investments.append(source)
    distributed_investments.append(target)
    return distributed_investments
