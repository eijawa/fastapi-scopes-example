from sqlalchemy.orm import sessionmaker

from .engine import engine


Session = sessionmaker(engine)
