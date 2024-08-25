from datetime import datetime, timedelta

from aiogoogle import Aiogoogle

from app.core.config import settings


async def set_user_permissions(
    spreadsheetid: str, wrapper_services: Aiogoogle
) -> None:
    """
    Выдать права аккаунту для работы с таблицами,
    которые находятся на диске сервисного аккаунта.
    """
    permissions_body = {
        "type": "user",
        "role": "writer",
        "emailAddress": settings.email,
    }
    service = await wrapper_services.discover(
        "drive",
        settings.GOOGLE_DRIVE_API_VERSION,
    )
    await wrapper_services.as_service_account(
        service.permissions.create(
            fileId=spreadsheetid, json=permissions_body, fields="id"
        )
    )


async def spreadsheets_create(wrapper_services: Aiogoogle) -> str:
    """Создать Google-таблицу и вернуть ее id."""
    service = await wrapper_services.discover(
        "sheets",
        settings.GOOGLE_SHEETS_API_VERSION,
    )
    spreadsheet_body = {
        "properties": settings.GOOGLE_TABLE_PROPERTIES,
        "sheets": [
            settings.GOOGLE_SHEETS_PROPERTIES,
        ],
    }
    response = await wrapper_services.as_service_account(
        service.spreadsheets.create(json=spreadsheet_body)
    )
    spreadsheetid = response["spreadsheetId"]
    return spreadsheetid


async def spreadsheets_update_value(
    spreadsheetid: str,
    charity_projects: list[tuple[str]],
    wrapper_services: Aiogoogle,
) -> None:
    """Обновить данные в Google-таблице."""
    now_date_time = datetime.now().strftime(settings.DATETIME_FORMAT)
    service = await wrapper_services.discover(
        "sheets",
        settings.GOOGLE_SHEETS_API_VERSION,
    )
    table_values = [
        ["Отчёт от", now_date_time],
        ["Топ проектов по скорости закрытия"],
        ["Название проекта", "Время сбора", "Описание"],
    ]
    for project in charity_projects:
        new_row = [
            project["name"],
            str(timedelta(days=project["completion_rate"])),
            project["description"],
        ]
        table_values.append(new_row)
    update_body = {
        "majorDimension": "ROWS",
        "values": table_values,
    }
    await wrapper_services.as_service_account(
        service.spreadsheets.values.update(
            spreadsheetId=spreadsheetid,
            range=settings.GOOGLE_TABLE_RANGE,
            valueInputOption="USER_ENTERED",
            json=update_body,
        )
    )
