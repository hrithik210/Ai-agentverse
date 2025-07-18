from passlib.context import CryptContext
from jose import JWTError, jwt
from datetime import datetime , timedelta
from fastapi import HTTPException, status, Depends
from fastapi.security import HTTPBearer , HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
from app.db.models import User
from app.db.database import get_db_session
import os
from dotenv import load_dotenv

load_dotenv()

secret_key = os.getenv("secret_key")
algorithm = "HS256"

pwd_context = CryptContext(schemes=['bcrypt'])
security = HTTPBearer()

def verify_password(plain_password , hashed_password):
  return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password):
  return pwd_context.hash(password)
