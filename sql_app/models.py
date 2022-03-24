from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from .database import Base


class User(Base):
    """
    Model of the User table in the database.

    ...

    Attributes
    ----------
    __tablename__ : name of the table to be used by SQLAlchemy DB
    id : int
        PRIMARY KEY - id of the user
    email : str
        email of the user
    hashed_password: str
        hashed version of the user's password
    is_active : bool
        flag reflecting the user's status
    items :
        SQL relation to the Items table
    """
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    is_active = Column(Boolean, default=True)

    items = relationship("Item", back_populates="owner")


class Item(Base):
    """
    Model of the Item table in the database.

    ...

    Attributes
    ----------
    __tablename__ : name of the table to be used by SQLAlchemy DB
    id : int
        PRIMARY KEY - id of the item
    title : str
        title of the item
    description : str
        description of the item
    owner_id : int
        id of the user that created the item
    owner :
        SQL relation to the Users table
    """
    __tablename__ = "items"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    description = Column(String, index=True)
    owner_id = Column(Integer, ForeignKey("users.id"))

    owner = relationship("User", back_populates="items")
