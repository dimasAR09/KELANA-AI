from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
import os

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://postgres:dimas09@127.0.0.1:5432/kelana_ai_db")
if "@Localhost" in DATABASE_URL:
    DATABASE_URL = DATABASE_URL.replace("@Localhost", "@127.0.0.1")

print(f"--> Membuka koneksi ke Database: {DATABASE_URL}" )

engine = create_engine(DATABASE_URL)

SessionLocal = sessionmaker(bind=engine, autoflush=False)

Base = declarative_base()

def init_db() -> None:
  """Create all SQLAlchemy tables for the configured database."""
  Base.metadata.create_all(bind=engine)

import models.user 
import models.trip
import models.conversation      
Base.metadata.create_all(bind=engine)