import sqlalchemy
from sqlalchemy.orm import sessionmaker
import models
import book
import publisher
import sale
import shop
import stock

DSN = 'postgresql://pumpkin:postgres@localhost:5432/py3_test'

engine = sqlalchemy.create_engine(DSN)

session = sessionmaker(bind=engine)()

models.create_tables(engine)

publisher_name = input('Введите имя издателя: ')

def gen_info(publisher_name):
    for res in session.query(book.Book.title, shop.Shop.name, sale.Sale.price, sale.Sale.date_sale).select_from(
        publisher.Publisher).join(book.Book, book.Book.id_publisher == publisher.Publisher.id).join(
            stock.Stock, stock.Stock.id_book == book.Book.id).join(shop.Shop, shop.Shop.id == stock.Stock.id_shop).join(
                sale.Sale, sale.Sale.id_stock == stock.Stock.id).filter(publisher.Publisher.name == publisher_name).all():
        print(f'{res[0]} | {res[1]} | {res[2]} | {res[3]}')


gen_info(publisher_name)
