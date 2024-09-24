from uuid import UUID
from fastapi import APIRouter, HTTPException, status, Depends, Body, Path, Query
from sqlalchemy.orm import Session
from typing import Annotated

from databases import database
from models import models
from utils import crud, oauth2_jwt


router = APIRouter(prefix='/api/v1', tags=['users'], dependencies=[Depends(oauth2_jwt.get_current_user)])


@router.get("/users/", response_model=list[models.User], tags=['users'], description='Retrieve all users.')
def find_users(
    limit: Annotated[int | None, Query(title='Limit', description='Paging limit variable.', ge=0, le=100)] = 10, 
    offset: Annotated[int | None, Query(title='Offset', description='Paging offset variable.', ge=0)] = 0, 
    db: Session = Depends(database.get_db)):

    return crud.get_users(db, offset=offset, limit=limit)


@router.get("/users/{id}", response_model=models.User, tags=['users'], description='Retrieve an user filtered by ID.')
def find_user(id: UUID = Path(description='User ID'), db: Session = Depends(database.get_db)):

    if db_user := crud.get_user(db, user_id=id):
        return db_user
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User with {id=} not found")
    

@router.post("/users/", response_model=models.User, tags=['users'], description='Add an User data.')
def create_user(user: Annotated[models.UserCreate, Body()] = None, db: Session = Depends(database.get_db)):

    if db_user := crud.get_user_by_email(db, email=user.email):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Email: {db_user.email} already registered")
    return crud.create_user(db=db, user=user)


@router.put("/users/{id}", response_model=models.User, tags=['users'], description='Update an User data by ID.')
def update_user(
    id: UUID = Path(description='User ID'), user: Annotated[models.UserUpdate, Body()] = None, 
    db: Session = Depends(database.get_db)):

    if user_updated := crud.update_user(db=db, user_id=id, user=user):
        return user_updated
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User with {id=} not found")


@router.delete("/users/{id}", status_code=status.HTTP_204_NO_CONTENT, tags=['users'], description='Delete an User by ID.')
def delete_user(id: UUID = Path(description='User ID'), db: Session = Depends(database.get_db)):

    if crud.delete_user(db=db, user_id=id):
        return
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User with {id=} not found")


@router.get("/weather/", response_model=list[models.Weather], description='Retrieve all weathers.')
def find_weathers(
    limit: Annotated[int | None, Query(title='Limit', description='Paging limit variable.', ge=0, le=100)] = 10, 
    offset: Annotated[int | None, Query(title='Offset', description='Paging offset variable.', ge=0)] = 0, 
    db: Session = Depends(database.get_db)):

    return crud.get_weathers(db, offset=offset, limit=limit)