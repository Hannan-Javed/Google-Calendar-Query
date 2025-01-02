import sqlite3

class DatabaseManager:
    def __init__(self, db_name='my-db.db'):
        self.db_name = db_name
        self.con = sqlite3.connect(self.db_name)
    
    def database_exists(self):
        cursor = self.con.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='CALENDAR';")
        return cursor.fetchone() is not None
    
    def create_database(self):
        self.con.execute("DROP TABLE IF EXISTS CALENDAR;")
        self.con.execute("""CREATE TABLE CALENDAR ( 
            id TEXT PRIMARY KEY NOT NULL, 
            summary TEXT,
            description TEXT,
            colorId INTEGER,
            reminders JSON,
            startTime TIMESTAMP,
            endTime TIMESTAMP,
            duration FLOAT
        );""")
        self.con.commit()

    def build_database(self, data):
        insert_query = """INSERT INTO CALENDAR 
            (id, summary, description, colorId, reminders, startTime, endTime, duration) 
            VALUES (?, ?, ?, ?, ?, ?, ?, ?);"""
        self.con.executemany(insert_query, [
            (
                event.get('id'),
                event.get('summary'),
                event.get('description'),
                event.get('colorId'),
                event.get('reminders'),
                event.get('startTime'),
                event.get('endTime'),
                event.get('duration')
            ) for event in data
        ])
        self.con.commit()
    
    def print_database(self):
        cursor = self.con.execute("SELECT * FROM CALENDAR;")
        for row in cursor:
            print(row)

    def query_database(self, query):
        cursor = self.con.execute(query)
        headers = [description[0] for description in cursor.description]
        results = cursor.fetchall()
        return headers, results
    
    def close_connection(self):
        self.con.close()