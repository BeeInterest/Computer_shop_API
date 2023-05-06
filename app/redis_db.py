from sqlalchemy import select

from execute_postgre import conn, account_table, client_table, worker_table

from db_redis.function_for_redis import request_postgre, Account, Worker, Client, RedisTools


class RedisData:
    count_data = {
        'Account': 0,
        'Worker': 0,
        'Client': 0
    }

    def completion_account(self):
        all_account = request_postgre(conn.execute(select(account_table)).fetchall())
        conn.commit()
        i = 0
        for row in all_account:
            account = Account(row[0], row[1])
            RedisTools.set_account(account, i)
            i += 1
        self.count_data['Account'] = i

    def completion_worker(self):
        all_worker = request_postgre(conn.execute(select(worker_table)).fetchall())
        conn.commit()
        i = 0
        for row in all_worker:
            worker = Worker(row[0], row[1], row[2], row[3], row[4], row[5], row[6])
            RedisTools.set_worker(worker, i)
            i += 1
        self.count_data['Worker'] = i

    def completion_client(self):
        all_client = request_postgre(conn.execute(select(client_table)).fetchall())
        conn.commit()
        i = 0
        for row in all_client:
            client = Client(row[0], row[1], row[2], row[3], row[4], row[5])
            RedisTools.set_client(client, i)
            i += 1
        self.count_data['Client'] = i

    def completion_redis(self):
        self.completion_client()
        self.completion_worker()
        self.completion_account()
        for key, value in self.count_data.items():
            self.count_data[key] -= 1

    def add_acc(self, login: str, password: str):
        self.count_data['Account'] += 1
        number = self.count_data['Account']
        print(number)
        account = Account(login, password)
        RedisTools.set_account(account, number)

    def add_worker(self, id_worker: str, full_name: str, phone: str, email: str, date_birth: str, position: str,
                   login: str):
        self.count_data['Worker'] += 1
        number = self.count_data['Worker']
        worker = Worker(id_worker, full_name, phone, email, date_birth, position, login)
        RedisTools.set_worker(worker, number)

    def add_client(self, id_client: str, full_name: str, phone: str, email: str, date_birth: str, login: str):
        self.count_data['Client'] += 1
        number = self.count_data['Client']
        client = Client(id_client, full_name, phone, email, date_birth, login)
        RedisTools.set_client(client, number)

    def del_acc(self):
        self.count_data['Account'] -= 1
        RedisTools.clear_redis('Account')
        self.completion_account()

    def del_client(self):
        self.count_data['Client'] -= 1
        RedisTools.clear_redis('Client')
        self.completion_client()

    def del_worker(self):
        self.count_data['Worker'] -= 1
        RedisTools.clear_redis('Worker')
        self.completion_worker()
