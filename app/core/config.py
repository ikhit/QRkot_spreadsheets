from typing import Optional

from pydantic import BaseSettings, EmailStr


class Settings(BaseSettings):
    """Класс для настроек проекта."""

    app_title: str = "QRKot"
    database_url: str = "sqlite+aiosqlite:///./fastapi.db"
    secret: str = "SECRET"
    first_superuser_email: Optional[EmailStr] = None
    first_superuser_password: Optional[str] = None
    type: Optional[str] = None
    project_id: Optional[str] = None
    private_key_id: Optional[str] = None
    private_key: Optional[str] = None
    client_email: Optional[str] = None
    client_id: Optional[str] = None
    auth_uri: Optional[str] = None
    token_uri: Optional[str] = None
    auth_provider_x509_cert_url: Optional[str] = None
    client_x509_cert_url: Optional[str] = None
    email: Optional[str] = None
    MAX_CHARITY_PROJECT_NAME_LEN: int = 100
    MIN_ANYSTR_LEN: int = 1
    CHARITY_PROJECT_NAME_EXAMPLE: str = "На корм кошечкам!"
    CHARITY_PROJECT_DESCRIPTION_EXAMPLE: str = "Сбор средств на покупку корма"
    CHARITY_PROJECT_FULL_AMOUNT_EXAMPLE: int = 1000
    DONATION_COMMENT_EXMAPLE: str = "Приятного аппетита котикам!"
    DONATION_FULL_AMOUNT_EXMAPLE: int = 100
    DEFAULT_INVESTED_AMOUNT: int = 0
    GOOGLE_DRIVE_API_VERSION: str = "v3"
    GOOGLE_SHEETS_API_VERSION: str = "v4"
    GOOGLE_SPREADSHEET_BASE_URL: str = (
        "https://docs.google.com/spreadsheets/d/"
    )
    USER_PERMISSIONS_BODY: dict = {
        "type": "user",
        "role": "writer",
    }
    DATETIME_FORMAT = "%Y/%m/%d %H:%M:%S"
    GOOGLE_TABLE_ROW_COUNT: int = 100
    GOOGLE_TABLE_COLUMN_COUNT: int = 10
    GOOGLE_SHEET_BODY: dict = {
        "properties": {
            "title": "Отчет по закрытым проектам",
            "locale": "ru_RU",
        },
        "sheets": [
            {
                "properties": {
                    "sheetType": "GRID",
                    "sheetId": 0,
                    "title": "Отчет по закрытым проектам",
                    "gridProperties": {
                        "rowCount": GOOGLE_TABLE_ROW_COUNT,
                        "columnCount": GOOGLE_TABLE_COLUMN_COUNT,
                    },
                },
            },
        ],
    }
    GOOGLE_TABLE_BASE: list[list[str]] = [
        ["Отчёт от"],
        ["Топ проектов по скорости закрытия"],
        ["Название проекта", "Время сбора", "Описание"],
    ]
    TABLE_FIRST_SQUARE: str = "A1"
    EMPTY_TABLE: str = f"{TABLE_FIRST_SQUARE}:{TABLE_FIRST_SQUARE}"
    COLUMN_INDEX_BASE: int = 64

    class Config:
        env_file = ".env"


settings = Settings()
