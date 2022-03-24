from sqlalchemy.orm import Session

from . import models, schemas


def get_user(db: Session, user_id: int):
    """
    Fetches user by id from the database
    :param db: database session
    :param user_id: id of the user to be fetched
    :return: User instance
    """
    return db.query(models.User).filter(models.User.id == user_id).first()


def get_user_by_email(db: Session, email: str):
    """
    Fetches user by email from the database
    :param db: database session
    :param email: email of the user to be fetched
    :return: User instance
    """
    return db.query(models.User).filter(models.User.email == email).first()


def get_users(db: Session, skip: int = 0, limit: int = 100):
    """
    Fetches multiple users from the database
    :param db: database session
    :param skip: query offset
    :param limit: query limit
    :return: list of users
    """
    return db.query(models.User).offset(skip).limit(limit).all()


def create_user(db: Session, user: schemas.UserCreate):
    """
    Creates a new User instance in the database session
    * the password is NOT hashed
    :param db: database session
    :param user: User instance containing the password
    :return: user instance saved in the database
    """
    fake_hashed_password = user.password + "notreallyhashed"
    db_user = models.User(email=user.email, hashed_password=fake_hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def get_items(db: Session, skip: int = 0, limit: int = 100):
    """
    Fetches multiple items from the database based on the offset and limit values
    :param db: database session
    :param skip: query offset
    :param limit: query limit
    :return: list of items
    """
    return db.query(models.Item).offset(skip).limit(limit).all()


def create_user_item(db: Session, item: schemas.ItemCreate, user_id: int):
    """
    Creates an item on behalf of the user
    :param db: database session
    :param item: Item instance
    :param user_id: id of the user creating the item
    :return: item instance saved in the database
    """
    db_item = models.Item(**item.dict(), owner_id=user_id)
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item
