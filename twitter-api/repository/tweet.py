# Python
from datetime import date

# Path
from models.tweet_api_model import Tweet
from models.user_api_model import User
from models.db_model import TweetDB

# SQLAlchemy
from sqlalchemy.orm import Session

# FastAPI
from fastapi import HTTPException, status


def get_all(db: Session):
    tweets = db.query(TweetDB).all()
    return tweets


def get(tweet_id: int, db: Session):
    tweet = db.query(TweetDB).filter(
        TweetDB.id == tweet_id
    ).first()

    if not tweet:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail="This tweet doesn't exist!"
        )

    return tweet


def create(tweet: Tweet, user: User, db: Session):
    new_tweet = tweet.dict()
    new_tweet['user_id'] = 1 # TODO get current user

    new_tweet = TweetDB(**new_tweet)
    db.add(new_tweet)
    db.commit()
    db.refresh(new_tweet)

    return tweet


def delete(tweet_id: int, db: Session):
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


def update(
    tweet_id: int,
    content: str, 
    db: Session
    ):
    tweet = db.query(TweetDB).filter(TweetDB.id == tweet_id)

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
