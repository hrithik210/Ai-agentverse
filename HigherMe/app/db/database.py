import psycopg2
import os
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv("DB_URL", "")


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
                sentiment TEXT,
                date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
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


if __name__ == "__main__":
    create_tables()
