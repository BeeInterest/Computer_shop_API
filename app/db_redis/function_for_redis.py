import redis

def request_postgre(cursor):
    result = []
    for row in cursor:
        row2 = list(map(str, list(row)))
        result.append(row2)
    return result


class Account:
    login = ""
    password = ""

    def __init__(self, login, passw):
        self.login = login
        self.password = passw


class Worker:
    id_worker = ""
    full_name = ""
    phone = ""
    email = ""
    date_birth_w = ""
    position = ""
    login_ac = ""

    def __init__(self, id_worker, name, phone, email, date, position, login):
        self.id_worker = id_worker
        self.full_name = name
        self.phone = phone
        self.email = email
        self.date_birth_w = date
        self.position = position
        self.login_ac = login


class Client:
    id_client = ""
    full_name = ""
    phone = ""
    email = ""
    date_birth = ""
    login_ac = ""

    def __init__(self, id_client, name, phone, email, date, login):
        self.id_client = id_client
        self.full_name = name
        self.phone = phone
        self.email = email
        self.date_birth = date
        self.login_ac = login


class RedisTools:
    __redis_connect = redis.StrictRedis(host='redis_db', port=6379, charset="utf-8", decode_responses=True)

    @classmethod
    def set_account(cls, account: Account, i: int):
        cls.__redis_connect.rpush(f"Account{i}", account.login, account.password)

    @classmethod
    def set_client(cls, client: Client, i: int):
        cls.__redis_connect.rpush(f"Client{i}", client.id_client, client.full_name, client.phone,
                                  client.email,
                                  client.date_birth, client.login_ac)

    @classmethod
    def set_worker(cls, worker: Worker, i: int):
        cls.__redis_connect.rpush(f"Worker{i}", worker.id_worker, worker.full_name, worker.phone,
                                  worker.email,
                                  worker.date_birth_w,
                                  worker.position, worker.login_ac)

    @classmethod
    def get_data(cls, key: str, count: int):
        return cls.__redis_connect.lrange(key, 0, count)

    @classmethod
    def get_keys(cls, who: str):
        return cls.__redis_connect.keys(pattern=f'{who}*')

    @classmethod
    def clear_redis(cls, who: str):
        for key in cls.__redis_connect.scan_iter(f"{who}*"):
            cls.__redis_connect.delete(key)



