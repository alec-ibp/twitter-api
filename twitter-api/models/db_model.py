# Path
from sqlalchemy.orm import relationship
from sqlalchemy.sql.schema import ForeignKey
from database import Base

# SQLAlchemy
from sqlalchemy import Column, Integer, String, Date, Text



class TweetDB(Base):
    __tablename__ = "tweets"

    id = Column(Integer, primary_key=True, index=True)

    content = Column(Text, nullable=False)
    created_at = Column(Date, nullable=False)
    updated_at = Column(Date, nullable=True)

    user_id = Column("user_id", Integer, ForeignKey("users.id"), nullable=False)

    author = relationship("UserDB", back_populates="tweets")

    def __init__(self, content, created_at, updated_at, user_id) -> None:
        self.content = content
        self.created_at = created_at
        self.updated_at = updated_at
        self.user_id = user_id


class UserDB(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)

    first_name = Column(String(32), nullable=False)
    last_name = Column(String(32), nullable=False)
    email = Column(String(128), nullable=False, unique=True)
    password = Column(String(128), nullable=False)
    birthday = Column(Date, nullable=False)

    tweets = relationship("TweetDB", back_populates="author")

    def __init__(self, first_name, last_name, email, password, birthday) -> None:
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.password = password
        self.birthday = birthday
