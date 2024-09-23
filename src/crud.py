import hashlib
from uuid import uuid4
from sqlalchemy.orm import Session
import models, schemas, oauth2_jwt


def get_user(db: Session, user_id: str):
    return db.query(schemas.User).filter(schemas.User.id == user_id).first()


def get_user_by_email(db: Session, email: str):
    return db.query(schemas.User).filter(schemas.User.email == email).first()


def get_users(db: Session, offset: int = 0, limit: int = 10):
    return db.query(schemas.User).offset(offset).limit(limit).all()


def create_user(db: Session, user: models.UserCreate):
    hashed_password = oauth2_jwt.get_password_hash(user.password)
    db_user = schemas.User(
        id=uuid4(), name=user.name, email=user.email,
        hashed_password=hashed_password
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def update_user(db: Session, user_id: str, user: models.UserUpdate):
    if db_user := db.query(schemas.User).filter(schemas.User.id == user_id).first():
        if user.name is not None:
            db_user.name = user.name
        if user.is_active is not None:
            db_user.is_active = user.is_active
        if user.password is not None:
            db_user.hashed_password = hashlib.sha3_256(user.password.encode()).hexdigest()
        
        db.commit()
        db.refresh(db_user)
        return db_user
    return None


def delete_user(db: Session, user_id: str):
    if db_user := db.query(schemas.User).filter(schemas.User.id == user_id).first():
        db.delete(db_user)
        db.commit()
        return True
    return False


def get_tasks(db: Session, offset: int = 0, limit: int = 100):
    return db.query(schemas.Task).offset(offset).limit(limit).all()


def get_task(db: Session, task_id: str):
    return db.query(schemas.Task).filter(schemas.Task.id == task_id).first()


def create_task(db: Session, task: models.TaskCreate):
    db_task = schemas.Task(
        id=uuid4(), name=task.name, 
        description=task.description
    )
    db.add(db_task)
    db.commit()
    db.refresh(db_task)
    return db_task


def create_user_task(db: Session, task: models.TaskCreate, user_id: str):
    if db.query(schemas.User).filter(schemas.User.id == user_id).first():
        db_task = schemas.Task(**task.dict(), id=uuid4(), owner_id=user_id)
        db.add(db_task)
        db.commit()
        db.refresh(db_task)
        return db_task
    return None


def get_user_tasks(db: Session, user_id: str, offset: int = 0, limit: int = 100):
    return db.query(schemas.Task).filter(schemas.Task.owner_id == user_id).offset(offset).limit(limit).all()


def update_task(db: Session, task_id: str, task: models.TaskUpdate):
    if db_task := db.query(schemas.Task).filter(schemas.Task.id == task_id).first():
        if task.name is not None:
            db_task.name = task.name
        if task.description is not None:
            db_task.description = task.description
        if task.status is not None:
            db_task.status = task.status
        
        db.commit()
        db.refresh(db_task)
        return db_task
    return None


def delete_task(db: Session, task_id: str):
    if db_task := db.query(schemas.Task).filter(schemas.Task.id == task_id).first():
        db.delete(db_task)
        db.commit()
        return True
    return False
