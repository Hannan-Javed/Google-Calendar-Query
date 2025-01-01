from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
import os

SCOPES = ['https://www.googleapis.com/auth/calendar']

class GoogleCalendarService:
    def __init__(self):
        self.creds = None
        self.service = None
        self.authenticate()

    def authenticate(self):
        if os.path.exists('token.json'):
            self.creds = Credentials.from_authorized_user_file('token.json', SCOPES)
        if not self.creds or not self.creds.valid:
            if self.creds and self.creds.expired and self.creds.refresh_token:
                self.creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
                self.creds = flow.run_local_server(port=0)
            with open('token.json', 'w') as token:
                token.write(self.creds.to_json())
        self.service = build('calendar', 'v3', credentials=self.creds)

    def fetch_events(self, start_date, end_date):
        all_events = []
        page_token = None
        while True:
            events = self.service.events().list(
                calendarId='primary',
                timeMin=start_date,
                timeMax=end_date,
                maxResults=2000,
                singleEvents=True,
                orderBy='startTime',
                pageToken=page_token
            ).execute()
            all_events.extend(events.get('items', []))
            if 'nextPageToken' in events:
                page_token = events['nextPageToken']
            else:
                break
        return all_events
