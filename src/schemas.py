from sqlalchemy import Boolean, Column, ForeignKey, String, UUID, DateTime, func
from sqlalchemy.orm import relationship

from database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(UUID, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    name = Column(String(100), index=True)
    hashed_password = Column(String)
    is_active = Column(Boolean, default=True)
    tasks = relationship("Task", back_populates="owner", cascade="all, delete", passive_deletes=True)

    created_at = Column(DateTime, index=True, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())


class Task(Base):
    __tablename__ = "tasks"

    id = Column(UUID, primary_key=True, index=True)
    name = Column(String(100), index=True)
    description = Column(String)
    status = Column(String(10), default='pending')

    owner_id = Column(UUID, ForeignKey("users.id", ondelete="CASCADE"), nullable=True)
    owner = relationship("User", back_populates="tasks")

    created_at = Column(DateTime, index=True, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())


class Weather(Base):
    __tablename__ = "weather"

    id = Column(UUID, primary_key=True, index=True)
    hostname = Column(String, index=True)
    country = Column(String)
    city = Column(String, nullable=True)
    weather = Column(String)
    temperature = Column(String, nullable=True)
    humidity = Column(String, nullable=True)
    wind_speed = Column(String, nullable=True)

    created_at = Column(DateTime, index=True, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())
