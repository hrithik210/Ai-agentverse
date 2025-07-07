from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from app.db.models import XPEvent, MoodLog, HealthLog, CodeLog, UserLevel
from langchain.llms import Groq
import os
from dotenv import load_dotenv

load_dotenv()