import os

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

username = os.getenv("DATABASE_USERNAME")
password = os.getenv("DATABASE_PASSWORD")
host = os.getenv("DATABASE_HOST")
database = os.getenv("DATABASE_NAME")

engine = create_engine(f"mysql+pymysql://{username}:{password}@{host}/{database}")

SessionLocal = sessionmaker()
SessionLocal.configure(bind=engine)

Base = declarative_base()
