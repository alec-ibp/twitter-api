# Path
from models.db_model import UserDB
from models.user_api_model import User, UserRegister
from database import get_db
from hashing import Hash
from JWT_token import create_access_token
# SQLAlchemy
from sqlalchemy.orm import Session

# FastAPI
from fastapi import APIRouter, Depends, Body
from fastapi import HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm

router = APIRouter(
    tags=['Authentication']
)

@router.post(
    path='/login',
    status_code=status.HTTP_200_OK,
    summary="Login a User",
)
def login(request: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = db.query(UserDB).filter(
        UserDB.email == request.username
    ).first()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"The user {request.username} doesn't exist"
        )
    
    if not Hash.verify(user.password, request.password):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Invalid Credentials"
        )

    access_token = create_access_token(data={'sub': user.email})
    return {"access_token": access_token, "token_type": "bearer"}



@router.post(
    path='/signup',
    response_model=User,
    status_code=status.HTTP_201_CREATED,
    summary="Register a User",
)
def sign_up(user: UserRegister = Body(...), db: Session = Depends(get_db)):
    """
    ## Sign up

    This path operation Create a user in the app

    ## Parameters:
    - Request Body parameter
        - user: UserRegister

    ## Returns a json with the basic user information (user model):
    - user_id: UUID
    - email: EmailStr
    - first_name: str
    - last_name: str
    - birthday: date
    """
    user.password = Hash.hash_password(user.password)
    new_user = UserDB(**user.dict())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user