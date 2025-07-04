import psycopg2
from datetime import datetime
from app.db.database import get_db

def create_code_log(lines_Added : int , lines_Removed : int , total_Time_Minutes : float):
    conn = get_db()
    if not conn:
        return None

    try:
        with conn.cursor() as cursor:
            cursor.execute(
                """
                INSERT INTO code_logs (lines_added, lines_removed, total_time_minutes, date)
                VALUES (%s, %s, %s, %s)
                RETURNING id;
                """,
                (lines_Added, lines_Removed, total_Time_Minutes, datetime.now())
            )
            code_log_id = cursor.fetchone()[0]
            conn.commit()
            return code_log_id
    except Exception as e:
        print(f"Error creating code log: {e}")
        return None
    finally:
        conn.close()

def create_health_log(meals: str, sleep_hours: float, exercise_minutes: int, water_intake_liter: float):
    conn = get_db()
    if not conn:
        return None

    try:
        with conn.cursor() as cursor:
            cursor.execute(
                """
                INSERT INTO health_logs (meals, sleep_hours, exercise_minutes, water_intake_liter, date)
                VALUES (%s, %s, %s, %s, %s)
                RETURNING id;
                """,
                (meals, sleep_hours, exercise_minutes, water_intake_liter, datetime.now())
            )
            health_log_id = cursor.fetchone()[0]
            conn.commit()
            return health_log_id
    except Exception as e:
        print(f"Error creating health log: {e}")
        return None
    finally:
        conn.close()

def create_mood_log(mood_text: str, sentiment: str):
    conn = get_db()
    if not conn:
        return None

    try:
        with conn.cursor() as cursor:
            cursor.execute(
                """
                INSERT INTO mood_logs (mood_text, sentiment, date)
                VALUES (%s, %s, %s)
                RETURNING id;
                """,
                (mood_text, sentiment, datetime.now())
            )
            mood_log_id = cursor.fetchone()[0]
            conn.commit()
            return mood_log_id
    except Exception as e:
        print(f"Error creating mood log: {e}")
        return None
    finally:
        conn.close()

def create_xp_event(xp_type: str, amount: int):
    conn = get_db()
    if not conn:
        return None

    try:
        with conn.cursor() as cursor:
            cursor.execute(
                """
                INSERT INTO xp_events (xp_type, amount, timestamp)
                VALUES (%s, %s, %s)
                RETURNING id;
                """,
                (xp_type, amount, datetime.now())
            )
            xp_event_id = cursor.fetchone()[0]
            conn.commit()
            return xp_event_id
    except Exception as e:
        print(f"Error creating XP event: {e}")
        return None
    finally:
        conn.close()

def get_or_create_level():
    conn = get_db()
    if not conn:
        return None

    try:
        with conn.cursor() as cursor:
            cursor.execute("SELECT * FROM levels LIMIT 1;")
            level = cursor.fetchone()

            if not level:
                cursor.execute(
                    """
                    INSERT INTO levels (current_level, total_xp, last_updated)
                    VALUES (%s, %s, %s)
                    RETURNING id;
                    """,
                    (1, 0, datetime.now())
                )
                conn.commit()
                level_id = cursor.fetchone()[0]
                return level_id
            return level
    except Exception as e:
        print(f"Error fetching or creating level: {e}")
        return None
    finally:
        conn.close()

def update_level(new_xp: int):
    conn = get_db()
    if not conn:
        return None

    try:
        with conn.cursor() as cursor:
            cursor.execute("SELECT * FROM levels LIMIT 1;")
            level = cursor.fetchone()

            if level:
                total_xp = level[2] + new_xp
                current_level = (total_xp // 100) + 1

                cursor.execute(
                    """
                    UPDATE levels
                    SET total_xp = %s, current_level = %s, last_updated = %s
                    WHERE id = %s;
                    """,
                    (total_xp, current_level, datetime.now(), level[0])
                )
                conn.commit()
                return level[0]
    except Exception as e:
        print(f"Error updating level: {e}")
        return None
    finally:
        conn.close()