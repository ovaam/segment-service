from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, Table
from sqlalchemy.orm import relationship
from .database import Base

user_segment = Table(
    'user_segment',
    Base.metadata,
    Column('user_id', Integer, ForeignKey('users.id'), primary_key=True),
    Column('segment_id', Integer, ForeignKey('segments.id'), primary_key=True)
)

class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    email = Column(String, unique=True, index=True)
    is_active = Column(Boolean, default=True)
    
    segments = relationship("Segment", secondary=user_segment, back_populates="users")

class Segment(Base):
    __tablename__ = "segments"
    
    id = Column(Integer, primary_key=True, index=True)
    slug = Column(String, unique=True, index=True)
    description = Column(String, nullable=True)
    is_active = Column(Boolean, default=True)
    
    users = relationship("User", secondary=user_segment, back_populates="segments")