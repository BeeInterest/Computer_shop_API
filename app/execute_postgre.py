from psycopg2 import OperationalError
from sqlalchemy import create_engine, Table, MetaData
import psycopg2

con = psycopg2.connect(
    database="computer_shop_postgre", user='postgres',
    password='1qwe2rty', host='postgres_db'
)
con.autocommit = True
cursor = con.cursor()
fd = open('db_postgres/db_postgres.sql', 'r', encoding='utf-8')
sql = fd.read()
fd.close()
sqlcom = sql.split(';')
for command in sqlcom:
    try:
        cursor.execute(sql)
    except OperationalError as msg:
        print("Command skipped: ", msg)
con.commit()
con.close()

engine = create_engine('postgresql://postgres:1qwe2rty@postgres_db/computer_shop_postgre')
meta = MetaData()

account_table = Table(
    'account',
    meta,
    extend_existing=True,
    autoload_with=engine
)

client_table = Table(
    'client',
    meta,
    extend_existing=True,
    autoload_with=engine
)

worker_table = Table(
    'worker',
    meta,
    extend_existing=True,
    autoload_with=engine
)

conn = engine.connect()
