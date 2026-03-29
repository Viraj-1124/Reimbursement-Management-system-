from sqlalchemy.orm import Session
import bcrypt
from jose import jwt, JWTError
from datetime import datetime, timedelta
from typing import Dict
from .models import User, RoleEnum
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from .database import get_db

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")

# Security Config
SECRET_KEY = "super_secret_key_change_in_production"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60 * 24 # 1 day

def verify_password(plain_password: str, hashed_password: str) -> bool:
    try:
        if isinstance(hashed_password, str):
            hashed_password = hashed_password.encode('utf-8')
        return bcrypt.checkpw(plain_password.encode('utf-8'), hashed_password)
    except Exception:
        return False

def get_password_hash(password: str) -> str:
    pwd_bytes = password.encode('utf-8')
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(pwd_bytes, salt)
    return hashed_password.decode('utf-8')

def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def register_user(db: Session, name: str, email: str, password: str) -> dict:
    """
    - Hash password
    - Create user
    - Generate JWT token
    Returns:
    {"user_id": str, "token": str}
    """
    db_user = db.query(User).filter(User.email == email).first()
    if db_user:
        raise ValueError("Email already registered")
        
    hashed_pwd = get_password_hash(password)
    new_user = User(
        name=name,
        email=email,
        password_hash=hashed_pwd,
        role=RoleEnum.EMPLOYEE # Default role
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    
    access_token = create_access_token(
        data={"sub": new_user.email, "user_id": str(new_user.id), "role": new_user.role.value}
    )
    
    return {"user_id": str(new_user.id), "token": access_token}

def login_user(db: Session, email: str, password: str) -> dict:
    """
    - Validate credentials
    - Return JWT token
    Returns:
    {"token": str, "role": str}
    """
    user = db.query(User).filter(User.email == email).first()
    if not user or not verify_password(password, user.password_hash):
        raise ValueError("Incorrect email or password")
        
    access_token = create_access_token(
        data={"sub": user.email, "user_id": str(user.id), "role": user.role.value}
    )
    
    return {"token": access_token, "role": user.role.value}

def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id: str = payload.get("user_id")
        if user_id is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    
    user = db.query(User).filter(User.id == user_id).first()
    if user is None:
        raise credentials_exception
    return user

def get_current_admin(current_user: User = Depends(get_current_user)):
    if current_user.role != RoleEnum.ADMIN:
        raise HTTPException(status_code=403, detail="Admin permissions required")
    return current_user

def get_current_manager(current_user: User = Depends(get_current_user)):
    if current_user.role not in [RoleEnum.ADMIN, RoleEnum.MANAGER]:
        raise HTTPException(status_code=403, detail="Manager permissions required")
    return current_user
