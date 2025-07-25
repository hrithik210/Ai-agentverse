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


def get_current_user(credentials : HTTPAuthorizationCredentials = Depends(security)):
  credential_exception = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="could not validate credentials",
    headers= {"WWW-Authenticate" : "Bearer"},
  )
  
  try:
    token = credentials.credentials
    payload = jwt.decode(token , secret_key , algorithms=[algorithm])
    username : str = payload.get("username")
    
    if username is None:
      raise credential_exception
  except JWTError:
    raise credential_exception
  
  db = get_db_session()
  
  try :
    user = db.query(User).filter(User.username == username).first()
    
    if user is None:
      raise credential_exception
    return user
  finally:
    db.close()