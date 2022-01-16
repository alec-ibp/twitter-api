# Python
from typing import List, Optional
from datetime import date

# Path
from models.user_api_model import User
from models.tweet_api_model import Tweet, ShowTweet
from models.db_model import TweetDB
from database import get_db
from oauth2 import get_current_user


# SQLAlchemy
from sqlalchemy.orm import Session

#FastAPI
from fastapi import APIRouter, Depends
from fastapi import Body, Path, Query, status, HTTPException


router = APIRouter(
    prefix='/home',
    tags=['Tweet']
)

@router.get(
    path='/',
    response_model=List[ShowTweet],
    status_code=status.HTTP_200_OK,
    summary="Show all tweets",
)
def home(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    """
    ## Home app

    This path operation show all tweets in the app

    ## Parameters:
  
    ## Returns a json list with all tweets in the app, with the following keys:
    - content: str
    - created_at: date
    - updated_at: Optional[date]
    - by: User
    """
    tweets = db.query(TweetDB).all()
    return tweets

### Post a tweet
@router.post(
    path='/',
    response_model=Tweet,
    status_code=status.HTTP_201_CREATED,
    summary="Post a Tweet",
)
def post_tweet(tweet: Tweet = Body(...), db: Session = Depends(get_db)):
    """
    ## Post a Tweet

    This path operation Create a tweet in the app

    ## Parameters:
    - Request Body parameter
        - tweet: Tweet

    ## Returns a json with the tweet information (tweet model):
    - content: str
    - created_at: date
    - updated_at: Optional[date]
    - by: User
    """

    new_tweet = tweet.dict()
    new_tweet['user_id'] = 1 # TODO get current user

    new_tweet = TweetDB(**new_tweet)
    db.add(new_tweet)
    db.commit()
    db.refresh(new_tweet)

    return tweet

### Show a tweet
@router.get(
    path='/{tweet_id}',
    response_model=ShowTweet,
    status_code=status.HTTP_200_OK,
    summary="Show a Tweet",
)
def show_a_tweet(
    tweet_id: str = Path(
        ..., 
        min_length=1,
        title='Tweet id',   
        description="this is the tweet id. Minimum characters: 1"
    ),
    db: Session = Depends(get_db)
    ):
    """
    ## Show a tweet

    this path parameter show a tweet of the app by the tweet_id

    ## Parameters:
    - path parameter
        - tweet_id: str
    
    ## Returns a json with the basic tweet information (tweet model):
    - content: str
    - created_at: date
    - updated_at: date
    - by: user
    """
    tweet = db.query(TweetDB).filter(
        TweetDB.id == tweet_id
    ).first()

    if not tweet:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail="This tweet doesn't exist!"
        )

    return tweet

### Delete a tweet
@router.delete(
    path='/{tweet_id}',
    status_code=status.HTTP_200_OK,
    summary="Delete a Tweet",
)
def delete_a_tweet(
    tweet_id: str = Path(
        ...,
        min_length=1,
        title='User id',
        description="this is the tweet id. Minimum characters: 1"
    ),
    db: Session = Depends(get_db)
    ):
    """
    ## Delete a tweet

    This path operation delete a tweet from the database

    ## Parameters:
    - path parameter:
        - tweet_id: str
    
    ## Returns None
    """
    tweet = db.query(TweetDB).filter(
        TweetDB.id == tweet_id)

    if not tweet.first():
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="This tweet doesn't exist!"
        )

    tweet.delete(synchronize_session=False)
    db.commit()

    return None

### Update a tweet
@router.put(
    path='/{tweet_id}',
    response_model=Tweet,
    status_code=status.HTTP_200_OK,
    summary="Update a Tweet",
)
def update_a_tweet(
    tweet_id: str = Path(
        ...,
        min_length=1,
        title='tweet id',
        description="this is the tweet id. Minimum characters: 1"
    ),
    content: Optional[str] = Query(
        default=None,
        min_length=1,
        max_length=256,
        title="Tweet content",
        description="This is content of the tweet, minimum characters: 1"
    ),
    db: Session = Depends(get_db)):
    """
    ## Update a tweet

    This path operation Update a tweet

    ## Parameters:
    - path parameter:
        - tweet_id: str
    - query parameters:
        - content: str
    
    ## Returns None
    """

    tweet = db.query(TweetDB).filter(
        TweetDB.id == tweet_id
    )

    if not tweet.first(): 
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="This tweet doesn't exist!"
        )
    tweet.update(
        {
            TweetDB.content: content,
            TweetDB.updated_at: str(date.today())
        }
    )

    db.commit()
    return None
