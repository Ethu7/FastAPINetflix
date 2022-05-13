from sqlite3 import Date
from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql.expression import text
from sqlalchemy.sql.sqltypes import TIMESTAMP

from .database import Base


class Title(Base):
    __tablename__ = "netflix_titles"

    show_id = Column(String, nullable=False, primary_key=True)
    type = Column(String, nullable=False)
    title = Column(String, nullable=False)
    director = Column(String)
    cast = Column(String)
    country = Column(String)
    date_added = Column(String)
    release_year = Column(Integer, nullable=False)
    rating = Column(String)
    duration = Column(String)
    listed_in = Column(String, nullable=False)
    description = Column(String, nullable=False)
    owner_id = Column(Integer, ForeignKey(
        "users.id", ondelete="CASCADE"), nullable=False)
    

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, nullable=False)
    email = Column(String, nullable=False, unique=True)
    password = Column(String, nullable=False)
    created_at = Column(TIMESTAMP(timezone=True),
                        nullable=False, server_default=text('now()'))
       