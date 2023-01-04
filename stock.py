import sqlalchemy as sq
from sqlalchemy.orm import relationship
import book
import shop
import models

class Stock(models.Base):
    __tablename__ = 'stock'

    id = sq.Column(sq.Integer, primary_key=True, autoincrement=True)

    id_book = sq.Column(sq.Integer, sq.ForeignKey('book.id'), nullable=False)

    id_shop = sq.Column(sq.Integer, sq.ForeignKey('shop.id'), nullable=False)

    count = sq.Column(sq.Integer)

    book = relationship(book.Book, backref='stock')
    shop = relationship(shop.Shop, backref='stock')
