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