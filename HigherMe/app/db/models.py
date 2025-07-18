from sqlalchemy import Column , Integer , String, DateTime, ForeignKey, Float, Boolean
from sqlalchemy.orm import relationship
from datetime import datetime
from .database import Base


class User(Base):
  __tablename__ = 'users'
  id = Column(Integer, primary_key=True, index=True)
  email = Column(String, unique=True, nullable=False)
  hashed_password = Column(String , nullable = False)
  created_at = Column(DateTime, default=datetime.now())
  is_active = Column(Boolean, default=True)
  
  #relations
  code_logs = relationship("CodeLog" , back_populates="user" , cascade="all, delete-orphan")
  health_logs = relationship("HealthLog" , back_populates="user" , cascade="all, delete-orphan")
  mood_logs = relationship("MoodLog" , back_populates="user" , cascade="all, delete-orphan")
  xp_events = relationship("XPEvent" , back_populates="user" , cascade="all, delete-orphan")
  level = relationship("Level" , back_populates="user" , cascade="all, delete-orphan")

class CodeLog(Base):
  __tablename__ = 'code_logs'
  id = Column(Integer, primary_key=True, index=True)
  lines_added = Column(Integer)
  lines_removed = Column(Integer)
  total_time_minutes = Column(Float)
  date = Column(DateTime, default=datetime.now)
  processed = Column(Boolean, default=False)
  processed_at = Column(DateTime, nullable=True)
  
  user = relationship("User" , back_populates="code_logs")

class HealthLog(Base):
  __tablename__ = 'health_logs'
  id = Column(Integer, primary_key = True , index=True)
  meals = Column(String)
  sleep_hours = Column(Float)
  exercise_minutes = Column(Integer)
  water_intake_liter = Column(Float)
  date = Column(DateTime, default=datetime.now)
  processed = Column(Boolean, default=False)
  processed_at = Column(DateTime, nullable=True)
  
  user = relationship("User" , back_populates="health_logs")

class MoodLog(Base):
    __tablename__ = "mood_logs"
    id = Column(Integer, primary_key=True, index=True)
    mood_text = Column(String)
    sentiment = Column(Float)
    timestamp = Column(DateTime, default=datetime.utcnow)
    processed = Column(Boolean, default=False)
    processed_at = Column(DateTime, nullable=True)
    
    user = relationship("User" , back_populates="mood_logs")
    
class XPEvent(Base):
    __tablename__ = "xp_events"
    id = Column(Integer, primary_key=True, index=True)
    xp_type = Column(String)
    amount = Column(Integer)
    timestamp = Column(DateTime, default=datetime.now)
    details = Column(String, nullable=True)
    
    user = relationship("User" , back_populates="xp_events")

class Level(Base):
    __tablename__ = "levels"
    id = Column(Integer, primary_key=True, index=True)
    current_level = Column(Integer, default=1)
    total_xp = Column(Integer, default=0)
    last_updated = Column(DateTime, default=datetime.now)
    
    user = relationship("User" , back_populates="level")
