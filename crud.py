from sqlalchemy.orm import Session

import models, schemas

def get_user(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.id == user_id).first()

def get_user_by_username(db: Session, username: str):
    return db.query(models.User).filter(models.User.username == username).first()

def get_user_by_email(db: Session, email: str):
    return db.query(models.User).filter(models.User.email == email).first()

def create_user(db: Session, user: schemas.UserCreate):
    hashed_password = user.password + "hashcode_op"
    db_user = models.User(username=user.username, email=user.email, password=hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def delete_user(db: Session, user: schemas.User):
    db.delete(user)
    db.commit()
    return

def create_catch_for_user(db: Session, catch: schemas.CatchCreate, user_id: int):
    db_catch = models.Catch(**catch.model_dump(), angler_id=user_id)
    db.add(db_catch)
    db.commit()
    db.refresh(db_catch)
    return db_catch

def delete_catch(db: Session, catch: schemas.Catch):
    db.delete(catch)
    db.commit()
    return
