import sqlite3, datetime as dt,sys
from config import TIME_ZONE, START_DATE, END_DATE
from google_calendar_service import GoogleCalendarService
from utils import filter_events

class DatabaseManager:
    def __init__(self, db_name='my-db.db'):
        self.db_name = db_name
        self.con = sqlite3.connect(self.db_name)
        self.create_database()
    
    def create_database(self):

        cursor = self.con.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='CALENDAR';")
        result = cursor.fetchone()

        if result is not None:
            cursor = self.con.execute("SELECT * FROM CALENDAR;")
            db_events = [dict(zip([column[0] for column in cursor.description], row)) for row in cursor.fetchall()]

        calendar_service = GoogleCalendarService()

        start_date = dt.datetime.strptime(START_DATE, "%d-%m-%Y")
        start_date = TIME_ZONE.localize(start_date).isoformat()
        end_date = dt.datetime.strptime(END_DATE, "%d-%m-%Y")
        end_date = TIME_ZONE.localize(end_date).isoformat()

        all_events = calendar_service.fetch_events(start_date, end_date)
        all_events = filter_events(all_events)

        if not all_events:
            print("No events found from start date till end date")
            sys.exit()

        if result is None or db_events is None or len(all_events) != len(db_events):
            self.create_table()
            self.build_database(all_events)
        else:
            changed = False
            for db_event, calendar_event in zip(db_events, all_events):
                if db_event != calendar_event:
                    changed = True
                    break

            if changed:
                self.create_table()
                self.build_database(all_events)

    def create_table(self):
        self.con.execute("DROP TABLE IF EXISTS CALENDAR;")
        self.con.execute("""CREATE TABLE CALENDAR ( 
            id TEXT PRIMARY KEY, 
            summary TEXT,
            description TEXT,
            colorId INTEGER NOT NULL,
            reminders JSON,
            startDate DATE NOT NULL,
            endDate DATE NOT NULL,
            startTime TIME NOT NULL,
            endTime TIME NOT NULL,
            day TEXT NOT NULL,
            duration FLOAT NOT NULL
        );""")
        self.con.commit()

    def build_database(self, data):
        insert_query = """INSERT INTO CALENDAR 
            (id, summary, description, colorId, reminders, startDate, endDate, startTime, endTime, day, duration) 
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);"""
        self.con.executemany(insert_query, [
            (
                event.get('id'),
                event.get('summary'),
                event.get('description'),
                event.get('colorId'),
                event.get('reminders'),
                event.get('startDate'),
                event.get('endDate'),
                event.get('startTime'),
                event.get('endTime'),
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