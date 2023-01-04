import sqlalchemy as sq
from sqlalchemy.orm import relationship
import models

class Sale(models.Base):
    __tablename__ = 'sale'

    id = sq.Column(sq.Integer, primary_key=True, autoincrement=True)

    price = sq.Column(sq.Integer)

    date_sale = sq.Column(sq.Date)

    id_stock = sq.Column(sq.Integer, sq.ForeignKey('stock.id'), nullable=False)

    count = sq.Column(sq.Integer)

    stock = relationship("Stock", backref='sale')
