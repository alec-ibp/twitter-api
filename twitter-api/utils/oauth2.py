# Path
from models.db_model import UserDB
from database import get_db
from .JWT_token import verify_token


#SQLAlchemy
from sqlalchemy.orm import Session

# FastAPI
from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from fastapi import HTTPException, status

oauth2_scheme = OAuth2PasswordBearer(tokenUrl='/login')

async def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"}
    )

    token_data =  verify_token(token, credentials_exception)
    
    user = db.query(UserDB).filter(
        UserDB.email == token_data.email
    ).first()

    if not user:
        raise credentials_exception
        
    return user