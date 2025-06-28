import os
import datetime
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from app.config import SCOPES, CREDENTIALS_FILE
from google.auth.transport.requests import Request  # Add this at the top

TOKEN_FILE = "app/token.json"

# Authenticate and return Google Calendar service
def get_calendar_service():
    creds = None

    if os.path.exists(TOKEN_FILE):
        creds = Credentials.from_authorized_user_file(TOKEN_FILE, SCOPES)

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(CREDENTIALS_FILE, SCOPES)

            # IMPORTANT: use fixed port 8080 and add it to Google Console
            creds = flow.run_local_server(port=8080)

        with open(TOKEN_FILE, "w") as token:
            token.write(creds.to_json())

    return build("calendar", "v3", credentials=creds)

# Optional helper: Check if time slot is free
def is_time_slot_free(start_time, end_time):
    service = get_calendar_service()
    body = {
        "timeMin": start_time.isoformat() + "Z",
        "timeMax": end_time.isoformat() + "Z",
        "items": [{"id": "primary"}],
    }
    events_result = service.freebusy().query(body=body).execute()
    return len(events_result["calendars"]["primary"]["busy"]) == 0

# Optional: Book event directly
def book_event(summary, start_time, end_time):
    service = get_calendar_service()
    event = {
        "summary": summary,
        "start": {"dateTime": start_time.isoformat(), "timeZone": "Asia/Kolkata"},
        "end": {"dateTime": end_time.isoformat(), "timeZone": "Asia/Kolkata"},
    }
    result = service.events().insert(calendarId="primary", body=event).execute()
    return result.get("htmlLink")
