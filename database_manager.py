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
            date DATE,
            startTime TIME,
            endTime TIME,
            day TEXT,
            duration FLOAT
        );""")
        self.con.commit()

    def build_database(self, data):
        insert_query = """INSERT INTO CALENDAR 
            (id, summary, description, colorId, reminders, date, startTime, endTime, day, duration) 
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?);"""
        self.con.executemany(insert_query, [
            (
                event.get('id'),
                event.get('summary'),
                event.get('description'),
                event.get('colorId'),
                event.get('reminders'),
                event.get('date').strftime('%d-%m-%Y'),
                event.get('startTime').strftime('%H:%M:%S'),
                event.get('endTime').strftime('%H:%M:%S'),
                event.get('day'),
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
    
    def format_results(self, headers, results):
        col_widths = [max(len(str(cell)) for cell in col) for col in zip(*([headers] + results))]
        print(" | ".join([f"{header:<{col_widths[i]}}" for i, header in enumerate(headers)]))
        print("-" * (sum(col_widths) + 3 * (len(headers) - 1)))
        for row in results:
            print(" | ".join([f"{str(cell):<{col_widths[i]}}" for i, cell in enumerate(row)]))
    
    def close_connection(self):
        self.con.close()