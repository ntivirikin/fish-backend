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
    
    db_user = crud.get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already exists!")

    return crud.create_user(db, user=user)

# Retrieve user information from database
@app.get("/users/{user_id}", response_model=schemas.User)
def read_user(user_id: int, db: Session = Depends(get_db)):
    db_user = crud.get_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User does not exist!")
    return db_user

# Delete user from database
@app.delete("/users/{user_id}")
def delete_user(user_id: int, db: Session = Depends(get_db)):
    db_user = crud.get_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User does not exist!")
    if len(db_user.catches) is not 0:
        raise HTTPException(status_code=400, detail="User still has catches that must be removed!")
    return crud.delete_user(db, user=db_user)

# Create catch for user
@app.post("/users/{user_id}/catches/", response_model=schemas.Catch)
def create_user_catches(user_id: int, catch: schemas.CatchCreate, db: Session = Depends(get_db)):
    db_user = crud.get_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User does not exist!")
    db_catch = crud.create_catch_for_user(db, catch=catch, user_id=user_id)
    return db_catch

# Retrieve catches by user
@app.get("/users/{user_id}/catches/", response_model=list[schemas.Catch])
def read_user_catches(user_id: int, db: Session = Depends(get_db)):
    db_user = crud.get_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User does not exist!")
    return db_user.catches

# Delete all catches
@app.delete("/users/{user_id}/catches/")
def delete_all_user_catches(user_id: int, db: Session = Depends(get_db)):
    db_user = crud.get_user(db, user_id=user_id)
    db_catches = db_user.catches
    for catch in db_catches:
        db_del = crud.delete_catch(db, catch)
    return db_del

# Delete catch from certain user
@app.delete("/users/{user_id}/catches/{catch_id}")
def delete_user_catch(user_id: int, catch_id: int, db: Session = Depends(get_db)):
    db_user = crud.get_user(db, user_id=user_id)
    if len(db_user.catches) is 0:
        raise HTTPException(status_code=404, detail="This user has no catches logged!")
    for catch in db_user.catches:
        if catch_id == catch.id:
            return crud.delete_catch(db, catch)
    raise HTTPException(status_code=404, detail="This user does not have this catch logged!")

# Sanity test for uvicorn
@app.get("/")
async def root():
    return {"message": "Hello World"}
