import datetime
import json
import random

from bson.json_util import dumps
from sqlalchemy import select
from execute_postgre import conn, client_table
from db_mongo.convert_uuid_bson import uuid_to_object_id
from db_mongo.init_mongo import comp_part, category, db


def request_db_id(cursor):
    json_data = dumps(cursor)
    all_info = json.loads(json_data)
    res = []
    for row in all_info:
        res.append(row["_id"])
    return res


class MongoTools:
    @classmethod
    def find_id(cls, key: str, value: str):
        all_id = request_db_id(category.find({key: value}))
        return all_id[0]

    @classmethod
    def random_id(cls):
        all_data = conn.execute(select(client_table)).fetchall()
        conn.commit()
        all_id = []
        for row in all_data:
            all_id.append(uuid_to_object_id(row[0]))
        r = random.randint(0, len(all_id) - 1)
        return all_id[r]

    @classmethod
    def find_id_client(cls, login: str):
        client_id_postgre = conn.execute(select(client_table).where(client_table.columns.login_ac == login)).fetchone()[0]
        conn.commit()
        return uuid_to_object_id(client_id_postgre)

    @classmethod
    def random_mongo_id(cls):
        all_data = request_db_id(comp_part.find())
        r = random.randint(0, len(all_data) - 1)
        return all_data[r]


db.comp_part.insert_many([
    {"name": "Жесткий диск Супер", "category_id": MongoTools.find_id("name_c", "Жесткий диск"), "price": 9999,
     "count": 200},
    {"name": "Жесткий диск ультра", "category_id": MongoTools.find_id("name_c", "Жесткий диск"), "price": 14999,
     "count": 100},
    {"name": "Процессор Мега", "category_id": MongoTools.find_id("name_c", "Процессор"), "price": 12999, "count": 400},
    {"name": "Процессор Гига", "category_id": MongoTools.find_id("name_c", "Процессор"), "price": 27999, "count": 50},
    {"name": "Материнская плата Биба", "category_id": MongoTools.find_id("name_c", "Материнская плата"), "price": 17999,
     "count": 102},
    {"name": "Материнская плата Боба", "category_id": MongoTools.find_id("name_c", "Материнская плата"), "price": 14999,
     "count": 103},
    {"name": "Видеокарта Пупа", "category_id": MongoTools.find_id("name_c", "Видеокарта"), "price": 60999, "count": 39},
    {"name": "Видеокарта Лупа", "category_id": MongoTools.find_id("name_c", "Видеокарта"), "price": 70999, "count": 57},
    {"name": "Охладитель Морозко", "category_id": MongoTools.find_id("name_c", "Охладитель"), "price": 8999,
     "count": 1000},
    {"name": "Охладитель ХолодноЧет", "category_id": MongoTools.find_id("name_c", "Охладитель"), "price": 6999,
     "count": 1001},
    {"name": "Оперативная память Весел", "category_id": MongoTools.find_id("name_c", "Оперативная память"),
     "price": 13999,
     "count": 245},
    {"name": "Оперативная память Боль", "category_id": MongoTools.find_id("name_c", "Оперативная память"),
     "price": 28999,
     "count": 307},
    {"name": "Блок питания Электроминус", "category_id": MongoTools.find_id("name_c", "Блок питания"), "price": 2999,
     "count": 206},
    {"name": "Блок питания КакПэчка", "category_id": MongoTools.find_id("name_c", "Блок питания"), "price": 1999,
     "count": 156},
    {"name": "Секрет", "category_id": MongoTools.find_id("name_c", "Секрет"), "price": 1000000, "count": 20},
])

db.comp_order.insert_many([
    {"client_id": MongoTools.random_id(), "date_order": datetime.datetime.utcnow(), "status": "принято",
     "basket": [{"comp_part_id": MongoTools.random_mongo_id(), "count": 1},
                {"comp_part_id": MongoTools.random_mongo_id(), "count": 2},
                {"comp_part_id": MongoTools.random_mongo_id(), "count": 1}]},
    {"client_id": MongoTools.random_id(), "date_order": datetime.datetime.utcnow(), "status": "не принято",
     "basket": [{"comp_part_id": MongoTools.random_mongo_id(), "count": 1},
                {"comp_part_id": MongoTools.random_mongo_id(), "count": 1},
                {"comp_part_id": MongoTools.random_mongo_id(), "count": 4}]},
    {"client_id": MongoTools.random_id(), "date_order": datetime.datetime.utcnow(), "status": "не принято",
     "basket": [{"comp_part_id": MongoTools.random_mongo_id(), "count": 1},
                {"comp_part_id": MongoTools.random_mongo_id(), "count": 1},
                {"comp_part_id": MongoTools.random_mongo_id(), "count": 1}]},
    {"client_id": MongoTools.random_id(), "date_order": datetime.datetime.utcnow(), "status": "принято",
     "basket": [{"comp_part_id": MongoTools.random_mongo_id(), "count": 1},
                {"comp_part_id": MongoTools.random_mongo_id(), "count": 2},
                {"comp_part_id": MongoTools.random_mongo_id(), "count": 1}]},
    {"client_id": MongoTools.random_id(), "date_order": datetime.datetime.utcnow(), "status": "принято",
     "basket": [{"comp_part_id": MongoTools.random_mongo_id(), "count": 1},
                {"comp_part_id": MongoTools.random_mongo_id(), "count": 2},
                {"comp_part_id": MongoTools.random_mongo_id(), "count": 1}]},
    {"client_id": MongoTools.random_id(), "date_order": datetime.datetime.utcnow(), "status": "принято",
     "basket": [{"comp_part_id": MongoTools.random_mongo_id(), "count": 6},
                {"comp_part_id": MongoTools.random_mongo_id(), "count": 1},
                {"comp_part_id": MongoTools.random_mongo_id(), "count": 6}]},
    {"client_id": MongoTools.random_id(), "date_order": datetime.datetime.utcnow(), "status": "принято",
     "basket": [{"comp_part_id": MongoTools.random_mongo_id(), "count": 1},
                {"comp_part_id": MongoTools.random_mongo_id(), "count": 1},
                {"comp_part_id": MongoTools.random_mongo_id(), "count": 2}]}
])

# query_comp_part = [('collMod', 'comp_part'),
#                  ('validator', {'name': {'$type': 'string'}}, {'category_id': {'$type': 'objectId'}},
#                  {'price': {'$type': 'int'}}, {'count': {'$type': 'int'}}),
#                   ('validationLevel', 'moderate')]
# query = OrderedDict(query_comp_part)
# db.command(query)

# query_category = [('collMod', 'category'),
#                  ('validator', {'name_c': {'$type': 'string'}}),
#                  ('validationLevel', 'moderate')]
# query = OrderedDict(query_category)
# db.command(query)

# query_comp_order = [('collMod', 'comp_order'),
#                    ('validator', {'client_id': {'$type': 'objectId'}}, {'date_order': {'$type': 'date'}},
#                     {'basket': {'$type': 'array'}},
#                     ({"comp_part_id": {'$type': 'objectId'}}, {"count": {'$type': 'int'}})),
#                    ('validationLevel', 'moderate')]
# query = OrderedDict(query_category)
# db.command(query)
