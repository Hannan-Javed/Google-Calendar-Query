# Google Calendar Query

## Overview
This project allows you to execute SQL queries on Google Calendar events. Since SQL queries cannot be executed directly using the Google Calendar API, the project first builds a database using SQLite3 after fetching the data from the Google Calendar API. It fetches events from a specified date range.

## Components
- **GoogleCalendarService**: Handles interactions with the Google Calendar API to fetch events.
- **DatabaseManager**: Manages database operations including building the database and executing queries.
- **Utils**: Contains utility functions.
- **Config**: Stores configuration settings.

## Database Schema
Table name is CALENDAR. Database schema is as follows:
- `id`: id of event. unique for each event
- `summary`: event title
- `description`: event description
- `colorId`: color id of event. Unique for each color (for common colors, see note below)
- `reminders`: reminder notifications in json format
- `startDate`: start date of event in the format `DD-MM-YYYY`
- `endDate`: end date of event in the format `DD-MM-YYYY`
- `startTime`: startTime of event
- `endTime`: endTime of event
- `day`: weekday of the event e.g. MON for Monday
- `duration`: duration of event in minutes (float)

## Installation
1. Clone the repository
    ```
    git clone https://github.com/Hannan-Javed/Google-Calendar-Query
    ```
2. Install the required packages:
    ```
    pip install -r requirements.txt
    ```
3. Enable the Google Calendar API for your project.
4. Create API credentials (OAuth 2.0 client ID) for your project.
5. Download the credentials.json file in the same directory as the python script.

You can also refer to the guideline here for Google project setup:<br>
https://www.youtube.com/watch?v=B2E82UPUnOY&t=463s

## Usage
To run the project, first create a `queries.sql` file that contains your queries. The format is shown with an example:
```
-- comments for what the query does (optional) e.g. displays sum of events for each day with colorId of 6
SELECT startDate, SUM(duration) as sum
FROM CALENDAR 
WHERE colorId = 6 
GROUP BY startDate;
```
The query can span over multiple lines but <b>must</b> end with `;`
Then run `main.py`. You can specify your date range.
Output for the example query is:
| startDate   | sum           |
|-------------|---------------|
| 01-12-2024  | 90.0          |
| 07-12-2024  | 120.0         |
| 10-12-2024  | 50.0          |
| 14-12-2024  | 270.0         |
| 21-12-2024  | 30.0          |
## Note
colorId mapping for common colors:
- `1`: <span style = "color: rgb(130,139,194)">Lavender</span>
- `2`: <span style = "color: rgb(85,176,128)">Sage</span>
- `3`: <span style = "color: rgb(176,90,186)">Grape</span>
- `4`: <span style = "color: rgb(214,131,122)">Falmingo</span>
- `5`: <span style = "color: rgb(231,186,81)">Banana</span>
- `6`: <span style = "color: rgb(227,104,62)">Tangerine</span>
- `7`: <span style = "color: rgb(75,153,210)">Peacock</span>
- `8`: <span style = "color: rgb(124,124,124)">Graphite</span>
- `9`: <span style = "color: rgb(110,114,195)">Blueberry</span>
- `10`: <span style = "color: rgb(72,145,96)">Basil</span>
- `11`: <span style = "color: rgb(218,82,52)">Tomato</span>