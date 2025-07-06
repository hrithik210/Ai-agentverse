from db.database import get_db
from app.db import crud
from sqlalchemy.orm import Session
from datetime import datetime
import os
from dotenv import load_dotenv

load_dotenv()
