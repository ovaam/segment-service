from sqlalchemy.orm import Session
from . import models
from .schemas import UserCreate, SegmentCreate, UserSegmentsUpdate
from .database import SessionLocal

def get_user(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.id == user_id).first()

def create_user(db: Session, user: UserCreate):
    db_user = models.User(**user.dict())
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def get_segment(db: Session, slug: str):
    return db.query(models.Segment).filter(models.Segment.slug == slug).first()

def create_segment(db: Session, segment: SegmentCreate):
    db_segment = models.Segment(**segment.dict())
    db.add(db_segment)
    db.commit()
    db.refresh(db_segment)
    return db_segment

def update_user_segments(db: Session, user_id: int, data: UserSegmentsUpdate):
    user = get_user(db, user_id)
    if not user:
        return None
    
    for slug in data.add_segments:
        segment = get_segment(db, slug)
        if segment and segment not in user.segments:
            user.segments.append(segment)
    
    for slug in data.remove_segments:
        segment = get_segment(db, slug)
        if segment and segment in user.segments:
            user.segments.remove(segment)
    
    db.commit()
    return user

def get_user_by_email(db: Session, email: str):
    return db.query(models.User).filter(models.User.email == email).first()