import psycopg2
from datetime import datetime
from app.db.database import get_db
from sqlalchemy.orm import Session
from app.db.models import CodeLog, HealthLog, MoodLog, XPEvent, Level
from app.db.database import get_db_session


def create_code_log(db: Session, *, lines_added: int, lines_removed: int, total_time_minutes: float, user_id: int):
    try:
        code_log = CodeLog(
            user_id=user_id,
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


def create_health_log(db: Session, *, meals: str, sleep_hours: float, exercise_minutes: int, water_intake_liter: float , user_id  : int):
    try:
        health_log = HealthLog(
            user_id=user_id,
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


def create_mood_log(db: Session, *, mood_text: str, sentiment: float, user_id: int):
    try:
        mood_log = MoodLog(
            user_id=user_id,
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




def award_xp(xp_type: str, amount: int, user_id: int):
    """
    Award XP for a particular type of event and update the level in one transaction.
    This function allows multiple XP awards per day for the same activity type,
    creating a cumulative gaming-like experience.

    Args:
        xp_type: The type of activity (e.g., "health", "mood", "coding")
        amount: The amount of XP to award
        user_id: The ID of the user earning XP

    Returns:
        The ID of the created XP event, or None if failed
    """

    db = get_db_session()

    try:
        # Create new XP event (no daily restriction)
        xp_event = XPEvent(
            user_id=user_id,
            xp_type=xp_type,
            amount=amount,
            timestamp=datetime.now()
        )

        db.add(xp_event)

        # Get or create level info for user
        level = db.query(Level).filter(Level.user_id == user_id).first()

        # Update level and XP
        if level:
            level.total_xp += amount
            level.current_level = (level.total_xp // 100) + 1
            level.last_updated = datetime.now()
        else:
            # Create initial level record if it doesn't exist
            level = Level(
                user_id=user_id, 
                total_xp=amount, 
                current_level=(amount // 100) + 1,
                last_updated=datetime.now()
            )
            db.add(level)

        db.commit()
        db.refresh(xp_event)
        
        print(f"Awarded {amount} XP for {xp_type} to user {user_id}. Total XP: {level.total_xp}, Level: {level.current_level}")
        
        return xp_event.id
        
    except Exception as e:
        db.rollback()
        print(f"Error awarding XP: {e}")
        return None
    finally:
        db.close()
