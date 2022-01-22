# Python
from typing import List, Optional

# Path
from models.user_api_model import User
from repository import user
from database import get_db

# SQLAlchemy
from sqlalchemy.orm import Session

# Pydantic
from pydantic import EmailStr

#FastAPI
from fastapi import APIRouter, Depends
from fastapi import Path, Query, status


router = APIRouter(
    prefix='/user',
    tags=['User']
)


@router.get(
    path='/',
    response_model=List[User],
    status_code=status.HTTP_200_OK,
    summary="Show all Users",
    )
def show_all_users(db: Session = Depends(get_db)):
    """
    ## Show all users
    This path operation show all the users in the app

    ## Returns a json list with all the users in the app, with the following keys
    - email: EmailStr
    - first_name: str
    - last_name: str
    - birthday: date
    """
    return user.get_all(db)


@router.get(
    path='/{id}',
    response_model=User,
    status_code=status.HTTP_200_OK,
    summary="Show a User",
    )
def show_a_user(id: int = Path(
    ...,
    gt=0,
    title='User id',
    description="this is the user id. Minimum characters: 1"
    ),
    db: Session = Depends(get_db)
    ):
    """
    ## Show a user
    this path parameter show a user of the app by the user_id

    ## Parameters:
    - path parameter
        - user_id: str
    
    ## Returns a json with the basic user information (user model):
    - email: EmailStr
    - first_name: str
    - last_name: str
    - birthday: date
    """
    return user.get(id, db)


@router.delete(
    path='/{id}',
    status_code=status.HTTP_200_OK,
    summary="Delete a User",
    )
def delete_a_user(id: int = Path(
    ...,
    gt=0,
    title='User id',
    description="this is the user id. Minimum characters: 1"
    ),
    db: Session = Depends(get_db)
    ):
    """
    ## Delete a user
    This path operation delete a user from the database

    ## Parameters:
    - path parameter:
        - user_id: str
    
    ## Returns None
    """
    return user.delete(id, db)


@router.put(
    path='/{id}',
    status_code=status.HTTP_200_OK,
    summary="Update a User",
    )
def update_a_user(
    id: int = Path(
    ...,
    gt=0,
    title='User id',
    description="this is the user id. Minimum characters: 1"
    ),
    first_name: Optional[str] = Query(
        default=None,
        min_length=1,
        max_length=50,
        title="First name",
        description="This is the first name of the user, minimum characters: 1"
    ),
    last_name: Optional[str] = Query(
        default=None,
        min_length=1,
        max_length=50,
        title="Last name",
        description="This is the last name of the user, minimum characters: 1"
    ),
    email: Optional[EmailStr] = Query(
        default=None,
        title="Email",
        description="This is the email of the user"
    ),
    db: Session = Depends(get_db)
    ):
    """
    ## Update a user
    This path operation Update a user

    ## Parameters:
    - path parameter:
        - user_id: str
    - query parameters:
        - first_name: str
        - last_name: str
        - email: EmailStr
    
    ## Returns None
    """

    user.update(id, first_name, last_name, email, db)