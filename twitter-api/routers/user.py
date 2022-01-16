# Python
from typing import List, Optional

# Path
from models.user_api_model import User, UserRegister
from models.db_model import UserDB

from database import get_db
from hashing import Hash

# SQLAlchemy
from sqlalchemy.orm import Session

# Pydantic
from pydantic import EmailStr

#FastAPI
from fastapi import APIRouter, Depends
from fastapi import Body, Path, Query, status, HTTPException


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

    ## Parameters:
    

    ## Returns a json list with all the users in the app, with the following keys
    - user_id: UUID
    - email: EmailStr
    - first_name: str
    - last_name: str
    - birthday: date
    """
    users = db.query(UserDB).all()
    return users


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

    this path parameter show a user of the app by the user_id (UUID)

    ## Parameters:
    - path parameter
        - user_id: str
    
    ## Returns a json with the basic user information (user model):
    - user_id: UUID
    - email: EmailStr
    - first_name: str
    - last_name: str
    - birthday: date
    """

    user = db.query(UserDB).filter(
        UserDB.id == id).first()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail="This user doesn't exist!"
            )
    
    return user


@router.delete(
    path='/{id}/delete',
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
    
    ## Returns a json with the following keys
    - user_id: UUID
    - email: EmailStr
    - first_name: str
    - last_name: str
    - birthday: date
    """
    user = db.query(UserDB).filter(
        UserDB.id == id)

    if not user.first():
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="This user doesn't exist!"
        )       

    user.delete(synchronize_session=False)
    db.commit()

    return None

### Update a user
@router.put(
    path='/{id}/update',
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
        -email: EmailStr
    
    ## Returns a json list with the following keys
    - user_id: UUID
    - email: EmailStr
    - first_name: str
    - last_name: str
    - birthday: date
    """

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