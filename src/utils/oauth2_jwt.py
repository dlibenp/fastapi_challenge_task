### OAuth2 with Password (and hashing), Bearer with JWT tokens
import os
from datetime import datetime, timedelta, timezone
from dotenv import load_dotenv
from typing import Annotated, Optional, List
from fastapi import Depends, APIRouter, HTTPException, status, Body, Path, Query
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from jose import JWTError, jwt
from passlib.context import CryptContext
from pydantic import BaseModel

from ..databases.database import Base, get_db as database_get_db
from ..models import models
from ..utils import crud

load_dotenv()  

router = APIRouter(tags=['auth'])

### AUTHENTICATE AND AUTHORIZED TOKEN OAUTH2-JWT - MODELS ###
class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    email: str | None = None


### CONFIGURE DEFAULT VARIABLES ###
# Random secret key used to sign JWT tokens. run: openssl rand -hex 32
SECRET_KEY = os.getenv('SECRET_KEY', '4bd037cebda1f8b35517b3d178a3363a012445dd281f6e0f704b1a9620dc4637')
ALGORITHM = os.getenv('ALGORITHM', 'HS256')
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv('ACCESS_TOKEN_EXPIRE_MINUTES', 30))

### HASH AND VERIFY PASSWORD UTILITIES ###
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

def verify_password(password, hashed_password):
    return pwd_context.verify(password, hashed_password)


def get_password_hash(password):
    return pwd_context.hash(password)


def authenticate_user(email: str, password: str, db: Session = Depends(database_get_db)):
    user_found = crud.get_user_by_email(db=db, email=email)
    
    if not user_found:
        return False
    if not verify_password(password, user_found.hashed_password):
        return False
    return user_found


# Create a utility function to generate a new access token.
def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


# Receive, decode and verify received JWT token, return current user or HTTP error if invalid.
async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)], 
    db: Session = Depends(database_get_db)):

    credentials_exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials", headers={"WWW-Authenticate": "Bearer"},)

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("sub")
        if email is None:
            raise credentials_exception
        token_data = TokenData(email=email)

    except JWTError:
        raise credentials_exception

    user_found = crud.get_user_by_email(db=db, email=token_data.email)
    if user_found is None:
        raise credentials_exception
    return user_found


async def get_current_active_user(current_user: Annotated[models.User, Depends(get_current_user)],):
    if not current_user.is_active:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user


# Create JWT access token, timedelta for expiration time.
@router.post("/token", response_model=Token)
async def login(form_data: Annotated[OAuth2PasswordRequestForm, Depends()], 
    db: Session = Depends(database_get_db)) -> Token:

    user = authenticate_user(email=form_data.username, password=form_data.password, db=db)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password", headers={"WWW-Authenticate": "Bearer"},)

    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(data={"sub": user.email}, expires_delta=access_token_expires)
    
    return Token(access_token=access_token, token_type="bearer")


@router.get("/users/me/", response_model=models.User)
async def read_users_me(current_user: Annotated[models.User, Depends(get_current_active_user)],):
    return current_user


@router.post("/users/me/", response_model=models.User)
def register(user: Annotated[models.UserCreate, Body()] = None, db: Session = Depends(database_get_db)):

    if db_user := crud.get_user_by_email(db, email=user.email):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Email: {db_user.email} already registered")
    return crud.create_user(db=db, user=user)
