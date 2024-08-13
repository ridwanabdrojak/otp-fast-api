from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from config.otp_config import Config

CONFIG=Config()
DATABASE_URL = f"postgresql+psycopg2://{CONFIG.db_user}:{CONFIG.db_pass}@{CONFIG.db_host}:{CONFIG.db_port}/{CONFIG.db_name}"

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
