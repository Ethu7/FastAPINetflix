from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional

from pydantic.types import conint


class UserOut(BaseModel):
    id: int
    email: EmailStr
    created_at: datetime

    class Config:
        orm_mode = True


class UserCreate(BaseModel):
    email: EmailStr
    password: str


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    id: Optional[str] = None



class TitleBase(BaseModel):
    show_id: str
    title: str
    release_year: int
    listed_in: str
    description: str

class Title(TitleBase):
    type: Optional[str]
    director: Optional[str]
    cast: Optional[str] = None
    country: Optional[str] = None
    date_added: Optional[str] = None
    rating: Optional[str] = None
    duration: Optional[str] = None
    owner_id: int
    owner: Optional[UserOut]

    class Config:
        orm_mode = True

class TitleCreate(TitleBase):
    pass


class TitleOut(Title):
    class Config:
        orm_mode = True

    