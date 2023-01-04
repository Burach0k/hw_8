import sqlalchemy as sq
from sqlalchemy.orm import declarative_base

Base = declarative_base()

def create_tables(engine):
    Base.metadata.create_all(engine)