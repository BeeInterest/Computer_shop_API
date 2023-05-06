from pymongo import MongoClient
from pymongo.collation import Collation

mongo = MongoClient('mongodb://mongo_db:27017')
db = mongo["computer_shop_mongo"]

db['comp_part'].drop()
db['category'].drop()
db['comp_order'].drop()

colla = Collation(
    locale="en_US",
    strength=2,
    numericOrdering=True,
    backwards=False
)

comp_part = db.create_collection(
    name="comp_part",
    codec_options=None,
    read_preference=None,
    write_concern=None,
    read_concern=None,
    session=None,
    collation=colla
)

category = db.create_collection(
    name="category",
    codec_options=None,
    read_preference=None,
    write_concern=None,
    read_concern=None,
    session=None,
    collation=colla
)

comp_order = db.create_collection(
    name="comp_order",
    codec_options=None,
    read_preference=None,
    write_concern=None,
    read_concern=None,
    session=None,
    collation=colla
)

db.category.insert_many([
    {"name_c": "Жесткий диск"},
    {"name_c": "Процессор"},
    {"name_c": "Материнская плата"},
    {"name_c": "Видеокарта"},
    {"name_c": "Охладитель"},
    {"name_c": "Оперативная память"},
    {"name_c": "Блок питания"},
    {"name_c": "Секрет"}
])