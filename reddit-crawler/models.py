from sqlalchemy import Column, String
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class Post(Base):
    __tablename__ = 'posts'
    title = Column(String, primary_key=True)
    author = Column(String)
    url = Column(String)
