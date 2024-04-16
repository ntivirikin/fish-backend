from sqlalchemy.orm import Session

import models, schemas

def get_user(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.id == user_id).first()

def get_user_by_username(db: Session, username: str):
    return db.query(models.User).filter(models.User.username == username).first()

def create_user(db: Session, user: schemas.UserCreate):
    hashed_password = user.password + "hashcode_op"
    db_user = models.User(username=user.username, email=user.email, password=hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def get_catches_by_user(db: Session, user_id: int):
    return db.query(models.Catch).filter(models.Catch.angler_id == user_id)

def create_catch_for_user(db: Session, catch: schemas.CatchCreate, user_id: int):
    db_catch = models.Catch(**catch.model_dump(), angler_id=user_id)
    db.add(db_catch)
    db.commit()
    db.refresh(db_catch)
    return db_catch