# Google Calendar Query

## Overview
This project allows you to execute SQL queries on Google Calendar events. Since SQL queries cannot be executed directly using the Google Calendar API, the project first builds a database using SQLite3 after fetching the data from the Google Calendar API. It fetches events from a specified date range.

## Components
- **GoogleCalendarService**: Handles interactions with the Google Calendar API to fetch events.
- **DatabaseManager**: Manages database operations including building the database and executing queries.
- **Utils**: Contains utility functions.
- **Config**: Stores configuration settings.

## Database Schema
The database schema is as follows:
- `id`: id of event. unique for each event
- `summary`: event title
- `description`: event description
- `colorId`: color id of event. Unique for each color (for common colors, see note below)
- `reminders`: reminder notifications in json format
- `startTime`: startTime of event
- `endTime`: endTime of event
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
To run the project, execute `main.py` function.
- You can specify your date range.
- You can write your SQL query. An example query is shown below that returns the total duration of all events with colorId `6`:

```SELECT SUM(duration) FROM CALENDAR WHERE colorId=6 GROUP BY colorId;```

### Note
colorId mapping for common colors:
- `1`: Lavender
- `2`: Sage
- `3`: Grape
- `4`: Falmingo
- `5`: Banana
- `6`: Tangerine
- `7`: Peacock
- `8`: Graphite
- `9`: Blueberry
- `10`: Basil
- `11`: Tomato