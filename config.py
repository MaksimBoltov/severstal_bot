from pydantic import BaseSettings


class TgAPISettings(BaseSettings):
    api_token: str

    class Config:
        env_prefix = "TG_"
        env_file = ".env"


class DBSettings(BaseSettings):
    engine: str
    user: str
    password: str
    host: str
    port: str
    database: str

    class Config:
        env_prefix = "DB_"
        env_file = ".env"


tg_api_settings = TgAPISettings()
db_settings = DBSettings()
