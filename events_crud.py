import uuid
import psycopg2


class EventsDbCRUDInterface:
    def create(self, record) -> str:
        pass

    def read(self, event_id):
        pass

    def update(self, event_id, record):
        pass

    def delete(self, event_id):
        pass

    def close(self):
        pass


class EventsMockDbCRUD(EventsDbCRUDInterface):
    def __init__(self):
        self.__db = {}
        self.table_name = "mockTable"

    def create(self, record) -> str:
        event_id = str(uuid.uuid4())
        formatted_keys = ', '.join([f'`{key}`' for key in record.keys()])
        formatted_values = ', '.join([f'`{value}`' for value in record.values()])
        insert_sql = f"'INSERT INTO {self.table_name} (event_id, {formatted_keys}) VALUES (`{event_id}`, {formatted_values})'"
        print(insert_sql)
        self.__db[event_id] = record
        return event_id

    def read(self, event_id):
        read_sql = f"'SELECT * FROM {self.table_name} WHERE event_id = `{event_id}`'"
        print(read_sql)
        res = self.__db.get(event_id)
        return res

    def update(self, event_id, record):
        record.pop('event_id', None)
        formatted_pairs = ', '.join([f'`{key}` = `{value}`' for key, value in record.items()])
        update_sql = f"'UPDATE {self.table_name} SET {formatted_pairs} WHERE event_id = `{event_id}`'"
        print(update_sql)
        self.__db[event_id] = record
        return event_id

    def delete(self, event_id):
        delete_sql = f"DELETE FROM events WHERE event_id = `{event_id}`"
        print(delete_sql)
        return self.__db.pop(event_id, None)

    def close(self):
        pass


def list_to_array(result):
    if result is None:
        return None
    output = dict()
    output['event_id'] = result[0]
    output['event'] = result[1]
    output['created_by'] = result[2]
    output['created_at'] = result[3]
    return output


class EventsDbCRUD(EventsDbCRUDInterface):
    def __init__(self, dbname, user, password, host, port):
        self.conn = psycopg2.connect(
            dbname=dbname,
            user=user,
            password=password,
            host=host,
            port=port
        )
        self.cur = self.conn.cursor()
        self.table_name = 'events'
        self.create_table_if_not_exists()

    def create_table_if_not_exists(self):
        # Check if the table exists, and if not, create it with columns based on dictionary keys
        self.cur.execute(f"CREATE TABLE IF NOT EXISTS {self.table_name} (event_id SERIAL PRIMARY KEY, event VARCHAR(50) NOT NULL, created_by VARCHAR(50), created_at TIMESTAMP DEFAULT current_timestamp);")
        self.conn.commit()

    def create(self, record) -> str:

        # Create dynamic SQL for inserting data and columns
        column_names = ', '.join(record.keys())
        values = ', '.join([f"'{value}'" for value in record.values()])

        self.cur.execute(f"INSERT INTO {self.table_name} ({column_names}) VALUES ({values}) RETURNING event_id")
        new_record_id = self.cur.fetchone()[0]

        self.conn.commit()

        return new_record_id

    def read(self, event_id):
        self.cur.execute(f"SELECT * FROM {self.table_name} WHERE event_id = {event_id}")
        result = self.cur.fetchone()
        return list_to_array(result)

    def update(self, event_id, record):
        record.pop('event_id', None)
        formatted_pairs = ', '.join([f'{key} = \'{value}\'' for key, value in record.items()])

        self.cur.execute(f"UPDATE {self.table_name} SET {formatted_pairs} WHERE event_id = {event_id}")
        self.conn.commit()
        return event_id

    def delete(self, event_id):
        result = self.read(event_id)
        self.cur.execute(f"DELETE FROM {self.table_name} WHERE event_id = {event_id}")
        self.conn.commit()
        return result

    def close(self):
        self.cur.close()
        self.conn.close()
