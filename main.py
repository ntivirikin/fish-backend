from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session

import crud, models, schemas
from database import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

# Used for Depends
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Create user
@app.post("/users/", response_model=schemas.User)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_username(db, username=user.username)
    if db_user:
        raise HTTPException(status_code=400, detail="Username already exists!")
    return crud.create_user(db, user=user)

# Retrieve user information from database
@app.get("/users/{user_id}", response_model=schemas.User)
def read_user(user_id: int, db: Session = Depends(get_db)):
    db_user = crud.get_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User does not exist!")
    return db_user

# Retrieve catches by user
@app.get("/users/{user_id}/catches/", response_model=list[schemas.Catch])
def read_user_catches(user_id: int, db: Session = Depends(get_db)):
    db_catches = crud.get_catches_by_user(db, user_id=user_id)
    if db_catches is None:
        raise HTTPException(status_code=404, detail="User does not exist!")
    return db_catches

# Retrieve catches by user
@app.post("/users/{user_id}/catches/", response_model=schemas.Catch)
def read_user_catches(user_id: int, catch: schemas.CatchCreate, db: Session = Depends(get_db)):
    db_catch = crud.create_catch_for_user(db, catch=catch, user_id=user_id)
    return db_catch

# Sanity test for uvicorn
@app.get("/")
async def root():
    return {"message": "Hello World"}

# Checks number of catches
# @app.get("/{user_id}/check")
@app.get("/check")
async def checkCatches():

    # Check DB here for catch number of user_id
    catches = 0
    return {"catches": catches}