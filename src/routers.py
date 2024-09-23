### OAuth2 with Password (and hashing), Bearer with JWT tokens
from uuid import uuid4
from datetime import datetime, timedelta, timezone
from typing import Annotated, Optional, List
from fastapi import Depends, APIRouter, HTTPException, status, Body, Path, Query
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy import Boolean, Column, String, UUID, DateTime, func
from sqlalchemy.orm import Session
from jose import JWTError, jwt
from passlib.context import CryptContext
from pydantic import BaseModel
from database import Base, get_db as database_get_db

router = APIRouter(tags=['auth-oauth2-jwt'])

### AUTHENTICATE AND AUTHORIZED USER OAUTH2-JWT - SCHEMAS ###
class UserAuthDb(Base):
    __tablename__ = "users_auth"

    id = Column(UUID, primary_key=True, index=True)  # sqlite postgresql - mysql(str)
    username = Column(String, unique=True, index=True)
    email = Column(String, unique=True, index=True)
    full_name = Column(String)
    hashed_password = Column(String)
    disabled = Column(Boolean, default=False)
    created_at = Column(DateTime, index=True, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())

### AUTHENTICATE AND AUTHORIZED USER OAUTH2-JWT - MODELS ###
# Pydantic Model used for token endpoint and response.
class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: str | None = None


class UserAuthBase(BaseModel):
    username: str
    email: str | None = None
    full_name: str | None = None
    disabled: bool | None = False
    created_at: datetime | None = None
    updated_at: datetime | None = None


class UserAuth(UserAuthBase):
    password: str

### SQLALCHEMY DATABASE USER OPPERATION - CRUD UTILITY ###
def get_user_by_username(db: Session, username: str):
    return db.query(UserAuthDb).filter(UserAuthDb.username == username).first()

def create_user(db: Session, user: UserAuth):
    hashed_password = get_password_hash(user.password)
    db_user = UserAuthDb(
        id=uuid4(), username=user.username, email=user.email, 
        full_name=user.full_name, hashed_password=hashed_password
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


### CONFIGURE DEFAULT VARIABLES ###
# Random secret key used to sign JWT tokens. run: openssl rand -hex 32
SECRET_KEY = "d6dc5020688adebd7d6b2b3202335aef19d25699de53983c73b11534c442fcdf"
ALGORITHM = "HS256"  # Algorithm used to sign the JWT token "HS256".
ACCESS_TOKEN_EXPIRE_MINUTES = 1  # Expiration of the token in minutes.

### HASH AND VERIFY PASSWORD UTILITIES ###
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="oauth2-jwt-token")

def verify_password(password, hashed_password):
    return pwd_context.verify(password, hashed_password)


def get_password_hash(password):
    return pwd_context.hash(password)


def authenticate_user(username: str, password: str, db: Session = Depends(database_get_db)):
    user = get_user_by_username(db=db, username=username)
    if not user:
        return False
    if not verify_password(password, user.hashed_password):
        return False
    return user


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
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)

    except JWTError:
        raise credentials_exception

    user = get_user_by_username(db=db, username=token_data.username)
    if user is None:
        raise credentials_exception
    return user


async def get_current_active_user(current_user: Annotated[UserAuthBase, Depends(get_current_user)],):
    if current_user.disabled:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user


# Create JWT access token, timedelta for expiration time.
@router.post("/oauth2-jwt-token", response_model=Token)
async def login_for_access_token(form_data: Annotated[OAuth2PasswordRequestForm, Depends()], 
    db: Session = Depends(database_get_db)) -> Token:

    user = authenticate_user(username=form_data.username, password=form_data.password, db=db)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password", headers={"WWW-Authenticate": "Bearer"},)

    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(data={"sub": user.username}, expires_delta=access_token_expires)
    
    return Token(access_token=access_token, token_type="bearer")


@router.get("/users/me/", response_model=UserAuthBase)
async def read_users_me(current_user: Annotated[UserAuthBase, Depends(get_current_active_user)],):
    return current_user


@router.post("/users/me/", response_model=UserAuthBase)
def create_users_me(user: Annotated[UserAuth, Body()] = None, db: Session = Depends(database_get_db)):

    if db_user := get_user_by_username(db, username=user.username):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Username: {db_user.username} already registered")
    return create_user(db=db, user=user)


def main():
    # $2b$12$XPlU5wa5GRFbrkEVIKzZse5jj1OG/9rDLzq/9kTClcnK0uE2Sfpke
    print('********* PASSWORD HASH *********', get_password_hash('admin'))

if __name__ == '__main__':
    # main()
    pass
