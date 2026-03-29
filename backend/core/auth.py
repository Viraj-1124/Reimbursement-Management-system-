from sqlalchemy.orm import Session
from passlib.context import CryptContext
from jose import jwt
from datetime import datetime, timedelta
from typing import Dict
from .models import User, RoleEnum

# Security Config
SECRET_KEY = "super_secret_key_change_in_production"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60 * 24 # 1 day

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password):
    return pwd_context.hash(password)

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
