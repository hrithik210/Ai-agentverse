from sqlalchemy.orm import Session
from . import models
from datetime import datetime

def create_code_log(db: Session , lines_Added : int , lines_Removed : int , total_Time_Minutes : float):
  code_log = models.CodeLog(
    lines_added = lines_Added,
    lines_removed = lines_Removed,
    total_time_minutes = total_Time_Minutes,
    date = datetime.now()
  )
  
  db.add(code_log)
  db.commit()
  db.refresh(code_log)
  return code_log

def create_health_log(db: Session, meals: str, sleep_hours: int, exercise_minutes: float, water_intake_liter: float):
  health_log = models.HealthLog(
    meals = meals,
    sleep_hours = sleep_hours,
    excercise_minutes = exercise_minutes,
    water_intake_liter = water_intake_liter,
    date = datetime.now()
  )
  
  db.add(health_log)
  db.commit()
  db.refresh(health_log)
  return health_log

def create_mood_log(db: Session, mood_text: str, sentiment: str):
  mood_log = models.MoodLog(
    mood_text = mood_text,
    sentiment = sentiment,
    date = datetime.now()
  )
  
  db.add(mood_log)
  db.commit()
  db.refresh(mood_log)
  return mood_log

def create_xp_event(db : Session , xp_type: str , amount : int ):
  xp_event = models.XPEvent(
    xp_type = xp_type,
    amount = amount,
    timestamp = datetime.now()
  )
  
  db.add(xp_event)
  db.commit()
  db.refresh(xp_event)
  return xp_event

def get_or_create_level(db : Session):
  level = db.query(models.Level).first()
  
  if not level:
    level = models.Level(
      current_level= 1,
      total_xp = 0,
      last_updated = datetime.now()
    )
    db.add(level)
    db.commit()
    db.refresh(level)
  return level


def update_level(db : Session , new_xp : int):
  level = get_or_create_level(db)
  
  level.total_xp += new_xp
  
   # level update: every 100 xp → +1 level
  level.current_level = (level.total_xp // 100) + 1
  level.last_updated = datetime.now()
  
  db.commit()
  db.refresh(level)
  return level