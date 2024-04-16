from sqlalchemy import Column, Integer, String, Date, ForeignKey
from sqlalchemy.orm import relationship

from database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    username = Column(String, unique=True, index=True)
    email = Column(String, unique=True)
    password = Column(String)

    catches = relationship("Catch", back_populates="angler")

class Catch(Base):
    __tablename__ = "catches"

    id = Column(Integer, primary_key=True)
    # date = Column(String)
    location = Column(String)
    species = Column(String)
    # length = Column(Integer)
    # weight = Column(Integer)
    angler_id = Column(Integer, ForeignKey("users.id"))

    angler = relationship("User", back_populates="catches")