from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from . import models, schemas, crud, services
from .database import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/segments/", response_model=schemas.Segment, status_code=201)
def create_segment(segment: schemas.SegmentCreate, db: Session = Depends(get_db)):
    db_segment = crud.get_segment(db, segment.slug)
    if db_segment:
        raise HTTPException(status_code=400, detail="Segment already exists")
    return crud.create_segment(db, segment)

@app.post("/segments/distribute/", status_code=200)
def distribute_segment(data: schemas.SegmentPercentage, db: Session = Depends(get_db)):
    try:
        count = services.distribute_segment(db, data.slug, data.percentage)
        return {"message": f"Segment {data.slug} distributed to {count} users"}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.post("/users/", response_model=schemas.User, status_code=201)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    try:
        db_user = crud.get_user_by_email(db, email=user.email)
        if db_user:
            raise HTTPException(status_code=400, detail="Email already registered")
        return crud.create_user(db, user=user)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/users/{user_id}", response_model=schemas.User)
def read_user(user_id: int, db: Session = Depends(get_db)):
    db_user = crud.get_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user

@app.post("/users/{user_id}/segments", response_model=schemas.User)
def update_user_segments(
    user_id: int, 
    segments_update: schemas.UserSegmentsUpdate, 
    db: Session = Depends(get_db)
):
    db_user = crud.update_user_segments(db, user_id, segments_update)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user