from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv("DB_URL", "")

engine = create_engine(DATABASE_URL, echo=True)

sessionLocal = sessionmaker(bind=engine)

Base = declarative_base()


def get_db():
  db = sessionLocal()
  try:
    yield db
  finally:
    db.close()


def test_db_connection():
  try:
    with engine.connect() as connection:
      print("Database connection successful!")
      return True
  except Exception as e:
    print(f"Database connection failed: {e}")
    return False




def create_tables():
    """Create all tables in the database."""
    Base.metadata.create_all(bind=engine)
    print("All tables created successfully!")

if __name__ == "__main__":
    create_tables()
