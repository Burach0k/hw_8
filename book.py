import sqlalchemy as sq
from sqlalchemy.orm import relationship
import publisher
import models

class Book(models.Base):
    __tablename__ = 'book'

    id = sq.Column(sq.Integer, primary_key=True, autoincrement=True)

    title = sq.Column(sq.String(length=100))

    id_publisher = sq.Column(sq.Integer, sq.ForeignKey('publisher.id'), nullable=False)

    publisher = relationship(publisher.Publisher, backref='book')