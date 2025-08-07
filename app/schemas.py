from pydantic import BaseModel
from typing import List, Optional

class SegmentBase(BaseModel):
    slug: str
    description: Optional[str] = None

class SegmentCreate(SegmentBase):
    pass

class Segment(SegmentBase):
    id: int
    is_active: bool
    class Config:
        orm_mode = True

class UserBase(BaseModel):
    username: str
    email: str

class UserCreate(UserBase):
    pass

class User(UserBase):
    id: int
    is_active: bool
    segments: List[Segment] = []
    class Config:
        orm_mode = True

class UserSegmentsUpdate(BaseModel):
    add_segments: List[str] = []
    remove_segments: List[str] = []

class SegmentPercentage(BaseModel):
    slug: str
    percentage: float