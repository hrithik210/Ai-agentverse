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

def create_health_log(db: Session, meals: str, sleep_hours: float, exercise_minutes: float, water_intake_liter: float):
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