from sqlalchemy import Column , Integer , String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from .database import Base

class User(Base):
  __tablename__ = 'code_logs'
  id = Column(Integer, primary_key=True, index=True)
  lines_added = Column(Integer)
  lines_removed = Column(Integer)
  total_time_minutes = Column(float)
  date = Column(DateTime, default=datetime.now)
  


class HealthLog(Base):
  __tablename__ = 'health_logs'
  id = Column(Integer, primary_key = True , index=True)
  meals = Column(String)
  sleep_hours = Column(float)
  excercise_minutes = Column(float)
  water_intake_liter = Column(float)
  date = Column(DateTime, default=datetime.now)
  
class MoodLog(Base):
    __tablename__ = "mood_logs"
    id = Column(Integer, primary_key=True, index=True)
    mood_text = Column(String)
    sentiment = Column(String)
    date = Column(DateTime, default=datetime.utcnow)