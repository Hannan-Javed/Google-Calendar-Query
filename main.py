import datetime as dt
from google_calendar_service import GoogleCalendarService
from database_manager import DatabaseManager
from utils import filter_events
from config import TIME_ZONE, START_DATE, END_DATE

def main():
    
    db_manager = DatabaseManager()
    if db_manager.database_exists():
        create_new_database = input("Database already exists. Do you want to create a new one and insert data, or use existing one? (new/old): ")
        if create_new_database == "new":
            db_manager.create_database()
            # fetch events from Google Calendar and build the database
            calendar_service = GoogleCalendarService()

            start_date = dt.datetime.strptime(START_DATE, "%d-%m-%Y")
            start_date = TIME_ZONE.localize(start_date).isoformat()
            end_date = dt.datetime.strptime(END_DATE, "%d-%m-%Y")
            end_date = TIME_ZONE.localize(end_date).isoformat()

            all_events = calendar_service.fetch_events(start_date, end_date)
            all_events = filter_events(all_events)
            
            db_manager.build_database(all_events)
    
    with open('queries.txt', 'r') as file:
        lines = file.read().splitlines()

    query = ''
    for line in lines:
        if line == '': continue
        elif line.startswith('--'):
            query_comment = line.strip()
        elif line.endswith(';'):
            query += line.strip()
            print(f"Query: {query_comment[2:].strip()}") if query_comment else None
            headers, results = db_manager.query_database(query)
            db_manager.format_results(headers, results)
            query_comment = ''
            query = ''
        else:
            query += line.strip() + ' '
    
if __name__ == '__main__':
    main()