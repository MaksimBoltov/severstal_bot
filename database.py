from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, scoped_session
from config import db_settings

SQLALCHEMY_DATABASE_URL = (
    f"{db_settings.engine}://{db_settings.user}:{db_settings.password}@"
    f"{db_settings.host}:{db_settings.port}/{db_settings.database}"
)

engine = create_engine(SQLALCHEMY_DATABASE_URL)
session = scoped_session(sessionmaker(bind=engine))
Base = declarative_base()
Base.query = session.query_property()
