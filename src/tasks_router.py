from uuid import UUID
from fastapi import APIRouter, HTTPException, status, Depends, Body, Path, Query
from sqlalchemy.orm import Session
from typing import Annotated
import crud, models, database
from oauth2_jwt import get_current_user


router = APIRouter(prefix='/api/v1', tags=['tasks'], dependencies=[Depends(get_current_user)])

@router.get("/tasks/", response_model=list[models.Task], tags=['tasks'], description='Retrieve all tasks.')
def find_tasks(
    limit: Annotated[int | None, Query(title='Limit', description='Paging limit variable.', ge=0, le=100)] = 10, 
    offset: Annotated[int | None, Query(title='Offset', description='Paging offset variable.', ge=0)] = 0, 
    db: Session = Depends(database.get_db)):

    return crud.get_tasks(db, offset=offset, limit=limit)


@router.get("/tasks/{id}", response_model=models.Task, tags=['tasks'], description='Retrieve a task filtered by ID.')
def find_task(id: UUID = Path(description='Tasks ID'), db: Session = Depends(database.get_db)):

    if db_task := crud.get_task(db, task_id=id):
        return db_task
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Task with {id=} not found")


@router.get("/tasks/users/{id}", response_model=list[models.Task], tags=['tasks'], description='Retrieve all User\'s tasks.')
def find_user_tasks(
    limit: Annotated[int | None, Query(title='Limit', description='Paging limit variable.', ge=0, le=100)] = 10, 
    offset: Annotated[int | None, Query(title='Offset', description='Paging offset variable.', ge=0)] = 0, 
    id: UUID = Path(description='User ID'), db: Session = Depends(database.get_db)):

    return crud.get_user_tasks(db=db, user_id=id, offset=offset, limit=limit)


@router.post("/tasks/", response_model=models.Task, tags=['tasks'], description='Add Task.')
def create_task(
    task: models.TaskCreate, db: Session = Depends(database.get_db)):

    if db_task := crud.create_task(db=db, task=task):
        return db_task
    raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Error creating a task")


@router.post("/tasks/users/{id}", response_model=models.Task, tags=['tasks'], description='Add User\'s task.')
def create_task_for_user(
    task: models.TaskCreate, id: UUID = Path(description='User ID'), 
    db: Session = Depends(database.get_db)):

    if user_task := crud.create_user_task(db=db, task=task, user_id=id):
        return user_task
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User with {id=} not found")


@router.put("/tasks/{id}", response_model=models.Task, tags=['tasks'], description='Update a Task by ID.')
def update_task(
    id: UUID = Path(description='Task ID'), task: Annotated[models.TaskUpdate, Body()] = None, 
    db: Session = Depends(database.get_db)):

    if task_updated := crud.update_task(db=db, task_id=id, task=task):
        return task_updated
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Task with {id=} not found")


@router.delete("/tasks/{id}", status_code=status.HTTP_204_NO_CONTENT, tags=['tasks'], description='Delete a Task by ID.')
def delete_task(id: UUID = Path(description='Task ID'), db: Session = Depends(database.get_db)):

    if crud.delete_task(db=db, task_id=id):
        return
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Task with {id=} not found")
