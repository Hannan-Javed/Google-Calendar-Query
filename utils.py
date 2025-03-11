import datetime as dt
import json
from config import TIME_ZONE
WEEKDAY = {0: 'MON', 1: 'TUE', 2: 'WED', 3: 'THU', 4: 'FRI', 5: 'SAT', 6: 'SUN'}

def filter_events(events):
    filtered_events = []
    props_to_remove = ['kind', 'etag', 'attendees', 'location', 'guestsCanInviteOthers', 'source', 'recurringEventId', 'transparency', 'visibility', 'status', 'htmlLink', 'created', 'updated', 'creator', 'organizer', 'sequence', 'iCalUID', 'eventType', 'originalStartTime']

    for event in events:
        if 'birthdayProperties' in event.keys():
            continue
        start_time = event['start'].get('dateTime', event['start'].get('date'))
        end_time = event['end'].get('dateTime', event['end'].get('date'))
        
        start_time = dt.datetime.fromisoformat(start_time).astimezone(TIME_ZONE)
        end_time = dt.datetime.fromisoformat(end_time).astimezone(TIME_ZONE)
        
        event['startTime'] = start_time
        event['endTime'] = end_time
        event['duration'] = (end_time - start_time).total_seconds() / 60  # duration in minutes
    
        event['startDate'] = start_time.date()
        event['endDate'] = end_time.date()
        event['startTime'] = start_time.time()
        event['endTime'] = end_time.time()
        event['day'] = WEEKDAY[dt.datetime.weekday(start_time)]

        event['reminders'] = json.dumps(event['reminders'])
        del event['start']
        del event['end']
        for prop in props_to_remove:
            if prop in event:
                del event[prop]
        if not 'summary' in event:
            event['summary'] = None
        if not 'description' in event:
            event['description'] = None
        if not 'colorId' in event:
            event['colorId'] = 1
        else:
            event['colorId'] = int(event['colorId'])
        filtered_events.append(event)
    return filtered_events