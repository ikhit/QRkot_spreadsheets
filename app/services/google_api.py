from datetime import datetime, timedelta

from aiogoogle import Aiogoogle

from app.core.config import settings


def get_table_range(table_values: list[list[str]]) -> str:
    """Получить количество используемых полей в таблице."""
    if not table_values:
        return settings.EMPTY_TABLE
    last_row = len(table_values)
    last_column_index = max([len(cell) for cell in table_values])
    if (
        last_row > settings.GOOGLE_TABLE_ROW_COUNT or
        last_column_index > settings.GOOGLE_TABLE_COLUMN_COUNT
    ):
        raise ValueError(
            "Количество данных в отчёте превышает размеры таблицы!",
        )
    last_column = chr(settings.COLUMN_INDEX_BASE + last_column_index)
    return (
        f"{settings.TABLE_FIRST_SQUARE}:{last_column}{last_row}"
        if last_column_index
        else settings.EMPTY_TABLE
    )


async def set_user_permissions(
    spreadsheet_id: str, wrapper_services: Aiogoogle
) -> None:
    """
    Выдать права аккаунту для работы с таблицами,
    которые находятся на диске сервисного аккаунта.
    """
    settings.USER_PERMISSIONS_BODY.update(
        {
            "emailAddress": settings.email,
        }
    )
    service = await wrapper_services.discover(
        "drive",
        settings.GOOGLE_DRIVE_API_VERSION,
    )
    await wrapper_services.as_service_account(
        service.permissions.create(
            fileId=spreadsheet_id,
            json=settings.USER_PERMISSIONS_BODY,
            fields="id",
        )
    )


async def spreadsheets_create(wrapper_services: Aiogoogle) -> str:
    """Создать Google-таблицу и вернуть ее id."""
    service = await wrapper_services.discover(
        "sheets",
        settings.GOOGLE_SHEETS_API_VERSION,
    )
    response = await wrapper_services.as_service_account(
        service.spreadsheets.create(json=settings.GOOGLE_SHEET_BODY)
    )
    spreadsheet_id = response["spreadsheetId"]
    spreadsheet_url = settings.GOOGLE_SPREADSHEET_BASE_URL + spreadsheet_id
    return spreadsheet_id, spreadsheet_url


async def spreadsheets_update_value(
    spreadsheet_id: str,
    charity_projects: list[tuple[str]],
    wrapper_services: Aiogoogle,
) -> None:
    """Обновить данные в Google-таблице."""
    now_date_time = datetime.now().strftime(settings.DATETIME_FORMAT)
    service = await wrapper_services.discover(
        "sheets",
        settings.GOOGLE_SHEETS_API_VERSION,
    )
    table_values = settings.GOOGLE_TABLE_BASE
    table_values[0].append(now_date_time)
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
    table_range = get_table_range(table_values)
    await wrapper_services.as_service_account(
        service.spreadsheets.values.update(
            spreadsheetId=spreadsheet_id,
            range=table_range,
            valueInputOption="USER_ENTERED",
            json=update_body,
        )
    )
