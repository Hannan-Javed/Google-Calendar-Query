import datetime as dt
from google_calendar_service import GoogleCalendarService
from database_manager import DatabaseManager
from utils import filter_events
from config import TIME_ZONE

def main():    
    calendar_service = GoogleCalendarService()
    start_date = "01-12-2024"
    end_date = "31-12-2024"

    start_date = dt.datetime.strptime(start_date, "%d-%m-%Y")
    start_date = TIME_ZONE.localize(start_date).isoformat()
    end_date = dt.datetime.strptime(end_date, "%d-%m-%Y")
    end_date = TIME_ZONE.localize(end_date).isoformat()

    all_events = calendar_service.fetch_events(start_date, end_date)
    all_events = filter_events(all_events)
    
    db_manager = DatabaseManager()
    db_manager.build_database(all_events)
    
    # sample query
    query = "SELECT SUM(duration) FROM CALENDAR WHERE colorId=6 GROUP BY colorId;"
    result = db_manager.query_database(query)
    for row in result:
        print(row)
    
if __name__ == '__main__':
    main()