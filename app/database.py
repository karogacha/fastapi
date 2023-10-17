from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from .config import settings

# SERVER = '.\SQLEXPRESS'
# DATABASE = 'fastapi'
# USERNAME = 'sa'
# PASSWORD = 'fgaror'

SQLALCHEMY_DATABASE_URL = f'mssql+pyodbc://{settings.database_username}:{settings.database_password}@{settings.database_server}/{settings.database_name}?driver=ODBC+Driver+17+for+SQL+Server&encoding=utf-8&azure=true'
# SQLALCHEMY_DATABASE_URL = f'mssql+pyodbc://{settings.database_username}:{settings.database_password}@{settings.database_server}/{settings.database_name}?driver=SQL+Server+Native+Client+11.0'
# SQLALCHEMY_DATABASE_URL = 'mssql+pyodbc://' + USERNAME + ':' + PASSWORD + '@' + SERVER + '/' + DATABASE + '?driver=SQL+Server+Native+Client+11.0'
# SQLALCHEMY_DATABASE_URL = "postgresql://user:password@postgresserver/db"

engine = create_engine(SQLALCHEMY_DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()