import psycopg2


def connect():
    connect = psycopg2.connect(
        database='py3_test', user='pumpkin', password='postgres')
    return connect, connect.cursor()
