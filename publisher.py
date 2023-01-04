import sqlalchemy as sq
import models

class Publisher(models.Base):
    __tablename__ = 'publisher'

    id = sq.Column(sq.Integer, primary_key=True, autoincrement=True)

    name = sq.Column(sq.String(length=40))
