import json
import datetime
import uuid
import uvicorn
from bson.json_util import dumps, ObjectId
from fastapi import FastAPI
from redis_db import RedisTools, RedisData
from models_mongo import db, MongoTools
from execute_postgre import conn, account_table, client_table, worker_table

app = FastAPI()

RedisDB = RedisData()
RedisDB.completion_redis()


def request_db(cursor):
    json_data = dumps(cursor)
    all_info = json.loads(json_data)
    res = []
    for document in all_info:
        document["_id"] = str(document["_id"])
        res.append(document)
    return res


def request_postgre(cursor):
    res = []
    for row in cursor:
        row2 = list(row)
        row2[0] = str(row2[0])
        res.append(row2)
    json_data = dumps(res, default=str)
    all_info = json.loads(json_data)
    result = []
    for row in all_info:
        result.append(row)
    return result


def account_exists(login, password):
    query_if = account_table.select().where(
        (account_table.columns.login_ac == login) & (account_table.columns.password_ac == password))
    if_result = conn.execute(query_if)
    conn.commit()
    access = ""
    for row in if_result:
        access += str(row)
    if access != "":
        return True
    else:
        return False


def user_not_exists(login):
    query_if_worker = worker_table.select().where(worker_table.columns.login_ac == login)
    query_if_client = client_table.select().where(client_table.columns.login_ac == login)
    if_result_worker = conn.execute(query_if_worker)
    conn.commit()
    if_result_client = conn.execute(query_if_client)
    access = ""
    for row in if_result_client:
        access += str(row)
    for row in if_result_worker:
        access += str(row)
    if access == "":
        return True
    else:
        return False


@app.get("/get_category")
async def get_category():
    all_category = db.category.find({})
    return request_db(all_category)


@app.get("/get_comp_parts")
async def get_comp_parts():
    all_comp_part = db.comp_part.find({})
    return request_db(all_comp_part)


@app.get("/get_comp_order")
async def get_comp_order():
    all_comp_order = db.comp_order.find({})
    return request_db(all_comp_order)


@app.get("/get_comp_part_cat/{category}")
async def get_comp_part_cat(category: str):
    all_comp_part_cat = db.comp_part.find({"category_id": db.category.find_one({"name_c": category})["_id"]})
    return request_db(all_comp_part_cat)


@app.get("/get_comp_part_keyword/{keyword}")
async def get_comp_part_keyword(keyword: str):
    all_comp_part_key = db.comp_part.find({"name": {'$regex': f'^{keyword}'}})
    return request_db(all_comp_part_key)


@app.get("/get_comp_part_price/start={start_price}end={end_price}")
async def get_comp_part_price(start_price: int, end_price: int):
    all_comp_part = db.comp_part.find({})
    all_comp_part_final = request_db(all_comp_part)
    res = []
    for b in all_comp_part_final:
        if start_price < b["price"] < end_price:
            res.append(b)
    return res


@app.post("/put_basket/client={id_client}-name={name_com}-count={count}")
async def put_basket(login: str, name_com: str, count: int):
    comp_part_id = db.comp_part.find_one({"name": name_com})["_id"]
    db.comp_order.insert_one(
        {"client_id": MongoTools.find_id_client(login), "date_order": datetime.datetime.utcnow(),
         "status": "в ожидании",
         "basket": [{"comp_part_id": ObjectId(comp_part_id), "count": count}]})
    db.comp_part.update_one({
        "name": name_com
    }, {
        "$inc": {
            "count": -count
        }
    })


@app.delete("/delete_order={id_order}", response_description="Delete an order")
async def delete_order(id_order: str):
    delete_result = db.comp_order.delete_one({"_id": ObjectId(id_order)})


@app.get("/get_client")
async def get_client():
    keys = RedisTools.get_keys('Client')
    data = []
    for row in keys:
        data.append(RedisTools.get_data(row, 5))
    return data


@app.get("/get_worker")
async def get_worker():
    keys = RedisTools.get_keys('Worker')
    data = []
    for row in keys:
        data.append(RedisTools.get_data(row, 6))
    return data


@app.get("/get_account")
async def get_account():
    keys = RedisTools.get_keys('Account')
    data = []
    for row in keys:
        data.append(RedisTools.get_data(row, 1))
    return data


@app.post("/create_account")
async def create_account(login: str, password: str):
    create_account = account_table.insert().values(login_ac=login, password_ac=password)
    conn.execute(create_account)
    conn.commit()
    RedisDB.add_acc(login, password)


@app.post("/create_client/")
async def create_client(login: str, full_name: str, phone: str, email: str, year: int, month: int,
                        day: int):
    if user_not_exists(login):
        id_client = uuid.uuid4()
        date_birth = datetime.date(year, month, day)
        create_client = client_table.insert().values(id_client=id_client, full_name=full_name, phone=phone,
                                                     email=email,
                                                     date_birth=date_birth, login_ac=login)
        conn.execute(create_client)
        conn.commit()
        RedisDB.add_client(str(id_client), full_name, phone, email, str(date_birth), login)
        return {"message": "Create client"}
    else:
        return {"message": "Login is busy"}


@app.post("/create_worker")
async def create_worker(login: str, full_name: str, phone: str, email: str, year: int, month: int,
                        day: int, position: str):
    if user_not_exists(login):
        id_worker = uuid.uuid4()
        date_birth_w = datetime.date(year, month, day)
        create_worker = worker_table.insert().values(id_worker=id_worker, full_name=full_name, phone=phone,
                                                     email=email,
                                                     date_birth_w=date_birth_w, position=position,
                                                     login_ac=login)

        conn.execute(create_worker)
        conn.commit()
        RedisDB.add_worker(str(id_worker), full_name, phone, email, str(date_birth_w), position, login)
        return {"message": "Create worker"}
    else:
        return {"message": "Login is busy"}


@app.delete("/delete_account")
async def delete_account(login: str, password: str):
    if account_exists(login, password):
        delete_account = account_table.delete().where(
            (account_table.columns.login_ac == login) & (account_table.columns.password_ac == password))
        conn.execute(delete_account)
        conn.commit()
        RedisDB.del_acc()
        return {"message": "Delete account"}
    else:
        return {"message": "Not exists"}


@app.delete("/delete_client")
async def delete_client(login: str, password: str):
    if account_exists(login, password):
        delete_client = client_table.delete().where(client_table.columns.login_ac == login)
        conn.execute(delete_client)
        conn.commit()
        RedisDB.del_client()
        delete_account = account_table.delete().where(
            (account_table.columns.login_ac == login) & (account_table.columns.password_ac == password))
        conn.execute(delete_account)
        conn.commit()
        RedisDB.del_acc()
        return {"message": "Delete client"}
    else:
        return {"message": "Not exists"}


@app.delete("/delete_worker")
async def delete_worker(login: str, password: str):
    if account_exists(login, password):
        delete_worker = worker_table.delete().where(worker_table.columns.login_ac == login)
        conn.execute(delete_worker)
        conn.commit()
        RedisDB.del_worker()
        delete_account = account_table.delete().where(
            (account_table.columns.login_ac == login) & (account_table.columns.password_ac == password))
        conn.execute(delete_account)
        conn.commit()
        RedisDB.del_acc()
        return {"message": "Delete worker"}
    else:
        return {"message": "Not exists"}


@app.get("/hello/{name}")
async def say_hello(name: str):
    return {"message": f"Hello {name}"}

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, log_level="info")
