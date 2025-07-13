import psycopg2
from datetime import datetime
from app.db.database import get_db
from sqlalchemy.orm import Session
from app.db.models import CodeLog, HealthLog, MoodLog, XPEvent, Level

def create_code_log(db: Session, *, lines_added: int, lines_removed: int, total_time_minutes: float):
    try:
        code_log = CodeLog(
            lines_added=lines_added,
            lines_removed=lines_removed,
            total_time_minutes=total_time_minutes,
            date=datetime.now(),
            processed=False
        )
        db.add(code_log)
        db.commit()
        db.refresh(code_log)
        return code_log
    except Exception as e:
        db.rollback()
        print(f"Error creating code log: {e}")
        return None

def create_health_log(db: Session, *, meals: str, sleep_hours: float, exercise_minutes: int, water_intake_liter: float):
    try:
        health_log = HealthLog(
            meals=meals,
            sleep_hours=sleep_hours,
            exercise_minutes=exercise_minutes,
            water_intake_liter=water_intake_liter,
            date=datetime.now(),
            processed=False
        )
        db.add(health_log)
        db.commit()
        db.refresh(health_log)
        return health_log
    except Exception as e:
        db.rollback()
        print(f"Error creating health log: {e}")
        return None

def create_mood_log(db: Session, *, mood_text: str, sentiment: float):
    try:
        mood_log = MoodLog(
            mood_text=mood_text,
            sentiment=sentiment,
            timestamp=datetime.now(),
            processed=False
        )
        db.add(mood_log)
        db.commit()
        db.refresh(mood_log)
        return mood_log
    except Exception as e:
        db.rollback()
        print(f"Error creating mood log: {e}")
        return None

def mark_logs_as_processed(db: Session, log_ids: list, log_type: str):
    """Mark multiple logs as processed"""
    try:
        now = datetime.now()
        if log_type == "mood":
            db.query(MoodLog).filter(MoodLog.id.in_(log_ids)).update({
                "processed": True,
                "processed_at": now
            })
        elif log_type == "health":
            db.query(HealthLog).filter(HealthLog.id.in_(log_ids)).update({
                "processed": True,
                "processed_at": now
            })
        elif log_type == "code":
            db.query(CodeLog).filter(CodeLog.id.in_(log_ids)).update({
                "processed": True,
                "processed_at": now
            })
        db.commit()
        return True
    except Exception as e:
        db.rollback()
        print(f"Error marking logs as processed: {e}")
        return False

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

def award_daily_xp(xp_type: str, amount: int):
    """
    Award XP for a particular type of event and update the level in one transaction.
    Checks if XP has already been awarded for this type today to prevent duplicates.
    
    Args:
        xp_type: The type of activity (e.g., "health", "mood", "coding")
        amount: The amount of XP to award
    
    Returns:
        The ID of the created XP event, or None if failed/duplicate
    """
    conn = get_db()
    if not conn:
        return None

    try:
        with conn.cursor() as cursor:
            # Check if XP has already been awarded for this type today
            today = datetime.now().date()
            cursor.execute(
                """
                SELECT id FROM xp_events 
                WHERE xp_type = %s AND DATE(timestamp) = %s
                LIMIT 1;
                """,
                (xp_type, today)
            )
            existing = cursor.fetchone()
            
            if existing:
                print(f"XP already awarded for {xp_type} today. Skipping.")
                return None
                
            # Begin a transaction to ensure both operations succeed or fail together
            cursor.execute("BEGIN;")
            
            # Create XP event
            cursor.execute(
                """
                INSERT INTO xp_events (xp_type, amount, timestamp)
                VALUES (%s, %s, %s)
                RETURNING id;
                """,
                (xp_type, amount, datetime.now())
            )
            xp_event_id = cursor.fetchone()[0]
            
            # Get current level info
            cursor.execute("SELECT * FROM levels LIMIT 1;")
            level = cursor.fetchone()

            if level:
                total_xp = level[2] + amount
                current_level = (total_xp // 100) + 1

                cursor.execute(
                    """
                    UPDATE levels
                    SET total_xp = %s, current_level = %s, last_updated = %s
                    WHERE id = %s;
                    """,
                    (total_xp, current_level, datetime.now(), level[0])
                )
            else:
                # Create initial level record if none exists
                cursor.execute(
                    """
                    INSERT INTO levels (current_level, total_xp, last_updated)
                    VALUES (%s, %s, %s);
                    """,
                    (1, amount, datetime.now())
                )
                
            # Commit the transaction
            cursor.execute("COMMIT;")
            return xp_event_id
            
    except Exception as e:
        # Roll back the transaction on error
        if conn:
            conn.execute("ROLLBACK;")
        print(f"Error awarding XP: {e}")
        return None
    finally:
        if conn:
            conn.close()