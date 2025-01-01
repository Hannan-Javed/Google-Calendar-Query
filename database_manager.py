import sqlite3

class DatabaseManager:
    def __init__(self, db_name='my-db.db'):
        self.db_name = db_name
    
    def create_database(self):
        con = sqlite3.connect(self.db_name)
        con.execute("DROP TABLE IF EXISTS CALENDAR;")
        con.execute("""CREATE TABLE CALENDAR ( 
            id TEXT PRIMARY KEY NOT NULL, 
            summary TEXT,
            description TEXT,
            colorId INTEGER,
            reminders JSON,
            startTime TIMESTAMP,
            endTime TIMESTAMP,
            duration FLOAT
        );""")
        con.close()
        
    def build_database(self, data):
        con = sqlite3.connect(self.db_name)
        for event in data:
            insert_query = "INSERT INTO CALENDAR (id, summary, description, colorId, reminders, startTime, endTime, duration) VALUES (?, ?, ?, ?, ?, ?, ?, ?);"
            con.execute(insert_query, (
                event.get('id'),
                event.get('summary'),
                event.get('description'),
                event.get('colorId'),
                event.get('reminders'),
                event.get('startTime'),
                event.get('endTime'),
                event.get('duration')
            ))
        con.commit()
        con.close()

    def print_database(self):
        con = sqlite3.connect(self.db_name)
        cursor = con.execute("SELECT * FROM CALENDAR;")
        for row in cursor:
            print(row)
        con.close()

    def query_database(self, query):
        con = sqlite3.connect(self.db_name)
        cursor = con.execute(query)
        result = cursor.fetchall()
        con.close()
        return result