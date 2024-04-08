from pydantic import BaseModel

class CatchBase(BaseModel):
    location: str
    species: str

class CatchCreate(CatchBase):
    pass

class Catch(CatchBase):
    id: int
    angler_id: int

    class Config:
        orm_mode = True

class UserBase(BaseModel):
    username: str
    email: str

class UserCreate(UserBase):
    password: str

class User(UserBase):
    id: int
    catches: list[Catch] = []

    class Config:
        orm_mode = True