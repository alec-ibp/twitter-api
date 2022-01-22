# OPath
from models.user_api_model import UserRegister
from models.db_model import UserDB
from hashing import Hash

# SQLAlchemy
from sqlalchemy.orm import Session

# Pydantic
from pydantic import EmailStr

# FastAPI
from fastapi import HTTPException, status


def create(user: UserRegister, db: Session):
    user.password = Hash.hash_password(user.password)

    new_user = UserDB(**user.dict())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user


def get_all(db: Session):
    users = db.query(UserDB).all()
    return users


def get(id: int, db: Session):
    user = db.query(UserDB).filter(
        UserDB.id == id).first()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail="This user doesn't exist!"
            )
    
    return user


def delete(id: int, db: Session):

    user = db.query(UserDB).filter(UserDB.id == id)

    if not user.first():
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="This user doesn't exist!"
        )       

    user.delete(synchronize_session=False)
    db.commit()

    return None


def update(
    id: int,
    first_name: str,
    last_name: str,
    email: EmailStr,
    db: Session
    ):

    user = db.query(UserDB).filter(
        UserDB.id == id
    )

    if not user.first():
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="This user doesn't exist!"
        )
    
    if not first_name: first_name = user.first().first_name
    if not last_name: last_name = user.first().last_name
    if not email: email = user.first().email

    user.update(
        {
            UserDB.first_name: first_name,
            UserDB.last_name: last_name,    
            UserDB.email: email
        }
    )

    db.commit()

    return None