import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from dotenv import load_dotenv

load_dotenv()

# host=os.getenv('DB_HOST')
# database=os.getenv('DB_NAME')
# user=os.getenv('DB_USER')
# password=os.getenv('DB_PASSWORD')
# port=os.getenv('DB_PORT')
DATABASE_URL = os.getenv("DATABASE_URL")

# SQLALCHEMY_DATABASE_URL = f"postgresql://{user}:{password}@{host}:{port}/{database}"

# engine = create_engine(f"postgresql://{user}:{password}@{host}:{port}/{database}")
engine = create_engine(DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()