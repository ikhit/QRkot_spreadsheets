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
    CHARITY_PROJECT_DESCRIPTION_EXAMPLE: str = "Сбор средств на покупку корма."
    CHARITY_PROJECT_FULL_AMOUNT_EXAMPLE: int = 1000
    DONATION_COMMENT_EXMAPLE: str = "Приятного аппетита котикам!"
    DONATION_FULL_AMOUNT_EXMAPLE: int = 100
    DEFAULT_INVESTED_AMOUNT: int = 0
    GOOGLE_DRIVE_API_VERSION: str = "v3"
    GOOGLE_SHEETS_API_VERSION: str = "v4"
    DATETIME_FORMAT = "%Y/%m/%d %H:%M:%S"
    GOOGLE_TABLE_RANGE: str = "A1:E30"
    GOOGLE_TABLE_PROPERTIES: dict = {
        "title": "Отчет по закрытым проектам.",
        "locale": "ru_RU",
    }
    GOOGLE_SHEETS_PROPERTIES: dict = {
        "properties": {
            "sheetType": "GRID",
            "sheetId": 0,
            "title": "Лист1",
            "gridProperties": {"rowCount": 100, "columnCount": 10},
        },
    }

    class Config:
        env_file = ".env"


settings = Settings()
