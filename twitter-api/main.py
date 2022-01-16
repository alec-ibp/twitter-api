# Path
from database import Base, engine
from routers import user, tweet, authentication
# fastAPI
from fastapi import FastAPI


Base.metadata.create_all(engine)
app = FastAPI()

app.include_router(user.router)
app.include_router(tweet.router)
app.include_router(authentication.router)