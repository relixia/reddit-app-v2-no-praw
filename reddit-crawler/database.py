from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

engine = create_engine('sqlite:///posts.db')
Session = sessionmaker(bind=engine)
