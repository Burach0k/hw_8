import sqlalchemy as sq
import models

class Shop(models.Base):
    __tablename__ = 'shop'

    id = sq.Column(sq.Integer, primary_key=True, autoincrement=True)

    name = sq.Column(sq.String(length=100))
