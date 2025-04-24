from sqlalchemy import Column, Integer, String, DateTime, LargeBinary, ForeignKey, Text, Index
from database.database import Base
from datetime import datetime
from sqlalchemy.orm import relationship
from datetime import datetime


class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    first_name = Column(String, index=True)
    last_name = Column(String, index=True)
    username = Column(String, nullable=False)
    email = Column(String, nullable=False)
    password_hashed = Column(String)
    Services = relationship("Services", back_populates="assignee")
    __table_args__ = (
        Index("ix_user_first_last_name", "first_name", "last_name"),
    )


class Orders(Base):
    __tablename__ = "orders"
    id = Column(Integer, primary_key=True)
    name = Column(String, index=True)
    description = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)
    Services = relationship("Services", back_populates="Orders")


class Services(Base):
    __tablename__ = "services"
    id = Column(Integer, primary_key=True)
    code = Column(String(50), unique=True, index=True)
    title = Column(String(100))
    description = Column(Text)
    service_id = Column(Integer, ForeignKey("service.id"))
    user_id = Column(Integer, ForeignKey("user.id"))
    created_at = Column(DateTime, default=datetime.utcnow)
    Orders = relationship("Orders", back_populates="Services")
    assignee = relationship("User", back_populates="Services")