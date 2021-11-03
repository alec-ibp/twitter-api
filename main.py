# Python
import json
from uuid import UUID
from typing import Optional, List
from datetime import date, datetime

# Pydantic
from pydantic import BaseModel
from pydantic import EmailStr
from pydantic import Field

# fastAPI
from fastapi import FastAPI
from fastapi import status
from fastapi import HTTPException
from fastapi import Body, Path, Query

app = FastAPI()

#Models
class UserBase(BaseModel):
    # unique identifier 
    user_id: UUID = Field(...)
    email: EmailStr = Field(...)


class UserLogin(UserBase):
    password: str = Field(
        ...,
        min_length=8,
        max_length=64
    )


class User(UserBase):
    first_name: str = Field(
        ...,
        min_length=2,
        max_length=50
    )
    last_name: str = Field(
        ...,
        min_length=2,
        max_length=50
    )
    birthday: Optional[date] = Field(default=None)


class UserRegister(User, UserLogin):
    pass


class Tweet(BaseModel):
    tweet_id: UUID = Field(...)
    content: str = Field(
        ...,
        min_length=1,
        max_length=256
    )
    created_at: datetime = Field(default=datetime.now())
    updated_at: Optional[datetime] = Field(default=None)
    # author
    by: User = Field(...)
    

# Path operations

## Users paths

### Register user
@app.post(
    path='/signup',
    response_model=User,
    status_code=status.HTTP_201_CREATED,
    summary="Register a User",
    tags=["Users"]
)
def sign_up(user: UserRegister = Body(...)):
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
    insert_to_file(entity='users', body_parameter=user)
    return user

### Login a user
@app.post(
    path='/login',
    response_model=User,
    status_code=status.HTTP_200_OK,
    summary="Login a User",
    tags=["Users"]
)
def login():
    pass

### Show all users
@app.get(
    path='/users',
    response_model=List[User],
    status_code=status.HTTP_200_OK,
    summary="Show all Users",
    tags=["Users"]
)
def show_all_users():
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
    results = read_file(entity='users')
    return results

### Show a user
@app.get(
    path='/users/{user_id}',
    response_model=User,
    status_code=status.HTTP_200_OK,
    summary="Show a User",
    tags=["Users"]
)
def show_a_user(user_id: str = Path(
    ...,
    min_length=1,
    title='User id',
    description="this is the user id. Minimum characters: 1"
    )
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
    results = read_file(entity='users')

    for user in results:
        if user['user_id'] == user_id:
            return user
    else:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail="This user doesn't exist!"
            )

### Delete a user
@app.delete(
    path='/users/{user_id}/delete',
    response_model=User,
    status_code=status.HTTP_200_OK,
    summary="Delete a User",
    tags=["Users"]
)
def delete_a_user(user_id: str = Path(
    ...,
    min_length=1,
    title='User id',
    description="this is the user id. Minimum characters: 1"
    )
    ):
    """
    ## Delete a user

    This path operation delete a user from the database

    ## Parameters:
    - path parameter:
        - user_id: str
    
    ## Returns a json list with all the users in the app, with the following keys
    - user_id: UUID
    - email: EmailStr
    - first_name: str
    - last_name: str
    - birthday: date
    """
    results = read_file(entity='users')
    for user in results:
        if user['user_id'] == user_id:
            results.remove(user)
            overwrite_file(entity='users', result_list=results)
            return user
    else:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="This user doesn't exist!"
        )        

### Update a user
@app.put(
    path='/users/{user_id}/update',
    response_model=User,
    status_code=status.HTTP_200_OK,
    summary="Update a User",
    tags=["Users"]
)
def update_a_user(
    user_id: str = Path(
    ...,
    min_length=1,
    title='User id',
    description="this is the user id. Minimum characters: 1"
    ),
    first_name: str = Query(
        default=None,
        min_length=1,
        max_length=50,
        title="First name",
        description="This is the first name of the user, minimum characters: 1"
    ),
    last_name: str = Query(
        default=None,
        min_length=1,
        max_length=50,
        title="Last name",
        description="This is the last name of the user, minimum characters: 1"
    ),
    email: EmailStr = Query(
        default=None,
        title="Email",
        description="This is the email of the user")
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
    
    ## Returns a json list with all the users in the app, with the following keys
    - user_id: UUID
    - email: EmailStr
    - first_name: str
    - last_name: str
    - birthday: date
    """

    results = read_file(entity='users')
    for user in results:
        if user['user_id'] == user_id:
            if first_name:
                user['first_name'] = first_name
            if last_name:
                user['last_name'] = last_name
            if email:
                user['email'] = email
            overwrite_file(entity='users', result_list=results)
            return user
    else:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="This user doesn't exist!"
        )
    
## Tweets paths

### Show all tweets
@app.get(
    path='/',
    response_model=List[Tweet],
    status_code=status.HTTP_200_OK,
    summary="Show all tweets",
    tags=['Tweets']
)
def home():
    """
    ## Home app

    This path operation show all tweets in the app

    ## Parameters:
  
    ## Returns a json list with all tweets in the app, with the following keys:
    - tweet_id: UUID
    - content: str
    - created_at: datetime
    - updated_at: Optional[datetime]
    - by: User
    """
    with open("tweets.json",'r',encoding='utf-8') as f:
        results = json.loads(f.read())
    return results

### Post a tweet
@app.post(
    path='/post',
    response_model=Tweet,
    status_code=status.HTTP_201_CREATED,
    summary="Post a Tweet",
    tags=["Tweets"]
)
def post_tweet(tweet: Tweet = Body(...)):
    """
    ## Post a Tweet

    This path operation Create a tweet in the app

    ## Parameters:
    - Request Body parameter
        - tweet: Tweet

    ## Returns a json with the tweet information (tweet model):
    - tweet_id: UUID
    - content: str
    - created_at: datetime
    - updated_at: Optional[datetime]
    - by: User
    """
    insert_to_file(entity='tweets', body_parameter=tweet)
    return tweet

### Show a tweet
@app.get(
    path='/tweets/{tweet_id}',
    response_model=Tweet,
    status_code=status.HTTP_200_OK,
    summary="Show a Tweet",
    tags=["Tweets"]
)
def show_a_tweet(tweet_id: str = Path(
     ...,
    min_length=1,
    title='Tweet id',
    description="this is the tweet id. Minimum characters: 1"
    )
    ):
    """
    ## Show a tweet

    this path parameter show a tweet of the app by the tweet_id (UUID)

    ## Parameters:
    - path parameter
        - tweet_id: str
    
    ## Returns a json with the basic tweet information (tweet model):
    - tweet_id: UUID
    - content: str
    - created_at: datetime
    - updated_at: datetime
    - by: user
    """
    results = read_file(entity='tweets')

    for tweet in results:
        if tweet['tweet_id'] == tweet_id:
            return tweet
    else:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail="This tweet doesn't exist!"
        )

### Delete a tweet
@app.delete(
    path='/tweets/{tweet_id}/delete',
    response_model=Tweet,
    status_code=status.HTTP_200_OK,
    summary="Delete a Tweet",
    tags=["Tweets"]
)
def delete_a_tweet():
    pass

### Update a tweet
@app.put(
    path='/tweets/{tweet_id}/update',
    response_model=Tweet,
    status_code=status.HTTP_200_OK,
    summary="Update a Tweet",
    tags=["Tweets"]
)
def update_a_tweet():
    pass


def read_file(entity: str):
    with open(entity + '.json', 'r', encoding='utf-8') as f:
        results = json.loads(f.read())
    return results

def overwrite_file(entity: str, result_list):
    with open(entity + '.json', 'w', encoding='utf-8') as f:
        f.write(json.dumps(result_list))

def insert_to_file(entity: str, body_parameter: Tweet):
    with open(entity + '.json', 'r+', encoding='utf-8') as f:
        results = json.loads(f.read()) # cast str -> json
        json_dict = body_parameter.dict()
        
        if entity == 'tweets':
            json_dict['tweet_id'] = str(json_dict['tweet_id']) # manual cast / fastapi can't cast uuid automatically
            json_dict['created_at'] = str(json_dict['created_at']) # manual cast / fastapi can't cast date automatically

            if len(str(json_dict['updated_at'])) > 0 :
                json_dict['updated_at'] = str(json_dict['updated_at']) # manual cast / fastapi can't cast date automatically
            json_dict['by']['user_id'] = str(json_dict['by']['user_id'])
            json_dict['by']['birthday'] = str(json_dict['by']['birthday'])

        else:
            json_dict['user_id'] = str(json_dict['user_id']) # manual cast / fastapi can't cast uuid automatically
            json_dict['birthday'] = str(json_dict['birthday'])
        
        results.append(json_dict)
        f.seek(0) # start writing at the beginning like overwrite
        f.write(json.dumps(results))
