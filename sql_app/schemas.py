from typing import Optional

from pydantic import BaseModel


class ItemBase(BaseModel):
    """
    Base schema for creation of an Item instance.

    ...

    Attributes
    ----------
    title : str
        title of the item
    description : str
        description of the item
    """
    title: str
    description: Optional[str] = None


class ItemCreate(ItemBase):
    """
    Schema for item creation.
    """
    pass


class Item(ItemBase):
    """
    Base schema for fetching an item instance from the database.

    ...

    Attributes
    ----------
    id : int
        id of the item
    owner_id : int
        id of the user that created the item

    Classes
    ----------
    Config :
        class for activating Pydantic's ORM mode
    """
    id: int
    owner_id: int

    class Config:
        orm_mode = True


class UserBase(BaseModel):
    """
    Base schema for creation of a User instance.

    ...

    Attributes
    ----------
    email : str
        email of the user
    """
    email: str


class UserCreate(UserBase):
    """
    Base schema for creation of a User instance.

    ...

    Attributes
    ----------
    password : str
        user's password
    """
    password: str


class User(UserBase):
    """
    Base schema for fetching a user instance from the database.

    ...

    Attributes
    ----------
    id : int
        id of the user
    is_active : bool
        flag reflecting the user's status
    items : list
        items created by the user

    Classes
    ----------
    Config :
        class for activating Pydantic's ORM mode
    """
    id: int
    is_active: bool
    items: list[Item] = []

    class Config:
        orm_mode = True
