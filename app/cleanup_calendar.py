import sys
import os
import datetime

# Add project root to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from app.calendar_utils import get_calendar_service

def delete_past_events():
    service = get_calendar_service()

    now = datetime.datetime.utcnow().isoformat() + "Z"  # Current time in UTC
    print("📆 Checking for events before:", now)

    # Fetch past events
    events_result = service.events().list(
        calendarId='primary',
        timeMax=now,
        singleEvents=True,
        orderBy='startTime'
    ).execute()

    events = events_result.get('items', [])

    if not events:
        print("✅ No past events to delete.")
        return

    print(f"🗑 Found {len(events)} past events. Deleting...")

    # Delete each past event
    for event in events:
        event_id = event['id']
        summary = event.get('summary', 'No Title')
        try:
            service.events().delete(calendarId='primary', eventId=event_id).execute()
            print(f"🗑 Deleted: {summary}")
        except Exception as e:
            print(f"❌ Failed to delete {summary}: {e}")

if __name__ == "__main__":
    delete_past_events()
