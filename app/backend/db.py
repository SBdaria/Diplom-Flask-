from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase

engine = create_engine('sqlite:///sunclothes.db', echo=True)

Session = sessionmaker(bind=engine)

db = Session()


class Base(DeclarativeBase):
    pass
