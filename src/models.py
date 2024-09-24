from pydantic import BaseModel, Field
from typing import Optional, List
from uuid import UUID, uuid4
from enum import Enum
from datetime import datetime

class StatusEnum(str, Enum):
    PENDING = 'pending'
    CREATED = 'created'
    INPROGRESS = 'in-progress'
    FINISHED = 'finished'


class TaskBase(BaseModel):
    name: str = Field(title='Name', max_length=100, min_length=4)
    description: str = Field(title='Description', min_length=10)
    status: StatusEnum = Field(title='Status', default=StatusEnum.PENDING)


class TaskCreate(TaskBase):
    pass


class TaskUpdate(TaskBase):
    name: Optional[str] = None
    description: Optional[str] = None
    status: Optional[StatusEnum] = None


class Task(TaskBase):
    id: UUID = Field(title='ID', default_factory=uuid4)
    owner_id: UUID | None = Field(title='Owner_ID', default_factory=uuid4)
    created_at: datetime | None = Field(title='CreatedAt', default=None)
    updated_at: datetime | None = Field(title='UpdatedAt', default=None)

    class Config:
        from_attributes = True


class UserBase(BaseModel):
    name: str
    email: str


class UserCreate(UserBase):
    password: str


class UserUpdate(BaseModel):
    email: Optional[str] = None
    name: Optional[str] = None
    password: Optional[str] = None
    is_active: Optional[bool] = None


class User(UserBase):
    id: UUID = Field(title='ID', default_factory=uuid4)
    is_active: bool | None = Field(title='IsActive', default=True)
    items: list[Task] = []
    created_at: datetime | None = Field(title='CreatedAt', default=None)
    updated_at: datetime | None = Field(title='UpdatedAt', default=None)

    class Config:
        from_attributes = True


class Weather(BaseModel):
    hostname: str
    country: str
    city: str | None = None
    weather: str
    temperature: str | None = None
    humidity: str | None = None
    wind_speed: str | None = None
