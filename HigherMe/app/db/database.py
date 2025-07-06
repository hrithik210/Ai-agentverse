import psycopg2
import os
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

load_dotenv()

DATABASE_URL = os.getenv("DB_URL", "")

# SQLAlchemy setup
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


def get_db_session():
    """Get SQLAlchemy session for ORM operations"""
    db = SessionLocal()
    try:
        return db
    except Exception as e:
        print(f"SQLAlchemy session failed: {e}")
        db.close()
        return None


def get_db():
    try:
        conn = psycopg2.connect(DATABASE_URL)
        return conn
    except Exception as e:
        print(f"Database connection failed: {e}")
        return None


def test_db_connection():
    conn = get_db()
    if conn:
        print("Database connection successful!")
        conn.close()
        return True
    else:
        return False


def create_tables():
    conn = get_db()
    if not conn:
        return

    try:
        with conn.cursor() as cursor:
            cursor.execute(
                """
            CREATE TABLE IF NOT EXISTS code_logs (
                id SERIAL PRIMARY KEY,
                lines_added INT,
                lines_removed INT,
                total_time_minutes FLOAT,
                date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );

            CREATE TABLE IF NOT EXISTS health_logs (
                id SERIAL PRIMARY KEY,
                meals TEXT,
                sleep_hours FLOAT,
                exercise_minutes INT,
                water_intake_liter FLOAT,
                date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );

            CREATE TABLE IF NOT EXISTS mood_logs (
                id SERIAL PRIMARY KEY,
                mood_text TEXT,
                sentiment FLOAT,
                timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );

            CREATE TABLE IF NOT EXISTS xp_events (
                id SERIAL PRIMARY KEY,
                xp_type TEXT,
                amount INT,
                timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );

            CREATE TABLE IF NOT EXISTS levels (
                id SERIAL PRIMARY KEY,
                current_level INT DEFAULT 1,
                total_xp INT DEFAULT 0,
                last_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
            """
            )
            conn.commit()
            print("All tables created successfully!")
    except Exception as e:
        print(f"Error creating tables: {e}")
    finally:
        conn.close()


def create_sqlalchemy_tables():
    """Create tables using SQLAlchemy ORM"""
    try:
        Base.metadata.create_all(bind=engine)
        print("SQLAlchemy tables created successfully!")
    except Exception as e:
        print(f"Error creating SQLAlchemy tables: {e}")


if __name__ == "__main__":
    create_tables()
    create_sqlalchemy_tables()
    create_sqlalchemy_tables()
