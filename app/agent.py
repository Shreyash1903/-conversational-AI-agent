import os
import json
import re
import datetime
from dotenv import load_dotenv
import google.generativeai as genai
from app.calendar_utils import get_calendar_service, is_time_slot_free
from app.config import GEMINI_API_KEY

# Load environment
load_dotenv()

# Configure Gemini
genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel("models/gemini-1.5-flash")


# Extract intent and meeting details
def extract_intent_and_details(text):
    today = datetime.date.today().strftime("%Y-%m-%d")

    prompt = f"""
Today is {today}.

You are a smart assistant that classifies user intent and extracts meeting details.

Only return valid JSON in one of these formats:

For booking a meeting:
{{
  "intent": "book",
  "title": "<meeting title>",
  "date": "YYYY-MM-DD",
  "time": "HH:MM"
}}

For checking if user is free:
{{
  "intent": "query_availability",
  "date": "YYYY-MM-DD",
  "time": "HH:MM"
}}

Important:
- If the user is asking "Can I schedule", "Am I free", or "Do I have time", return intent as "query_availability"
- If the title is not clear (like in availability queries), use null for title or skip it
- Use today's date to resolve words like "tomorrow", "next Monday", etc.
- Do not include markdown, triple backticks, or explanations.

User Input: {text}
"""
    response = model.generate_content(prompt)
    content = response.text.strip()
    content = re.sub(r"^```(?:json)?|```$", "", content).strip()

    print("📦 Extracted JSON raw:\n", content)
    return content


# ✅ Book a meeting after checking availability
def create_calendar_event(title: str, date: str, time: str) -> str:
    try:
        dt_start = datetime.datetime.fromisoformat(f"{date}T{time}:00")
        dt_end = dt_start + datetime.timedelta(hours=1)

        now = datetime.datetime.now()
        if dt_start < now:
            return f"❌ Cannot book a meeting in the past. Please choose a future time."

        # ✅ Check if time is already booked
        if not is_time_slot_free(dt_start, dt_end):
            return f"❌ A meeting already exists on {date} at {time}. Please select another time slot."

        service = get_calendar_service()
        event = {
            "summary": title,
            "start": {"dateTime": dt_start.isoformat(), "timeZone": "Asia/Kolkata"},
            "end": {"dateTime": dt_end.isoformat(), "timeZone": "Asia/Kolkata"},
        }

        created_event = service.events().insert(calendarId="primary", body=event).execute()
        return f"✅ Meeting scheduled: {created_event.get('htmlLink')}"

    except Exception as e:
        return f"❌ Failed to schedule meeting: {str(e)}"


# Check if time is free
def check_availability(date: str, time: str) -> str:
    try:
        start_time = datetime.datetime.fromisoformat(f"{date}T{time}:00")
        end_time = start_time + datetime.timedelta(hours=1)

        available = is_time_slot_free(start_time, end_time)
        if available:
            return f"✅ You are free on {date} at {time}."
        else:
            return f"❌ You already have a meeting on {date} at {time}."

    except Exception as e:
        return f"❌ Error while checking availability: {str(e)}"


# Main handler
def handle_user_message(user_input: str) -> str:
    try:
        extracted = extract_intent_and_details(user_input)
        data = json.loads(extracted)

        print("📋 Parsed Intent + Data:", data)
        intent = data.get("intent")

        if intent == "book":
            title = (data.get("title") or "").strip()
            date = (data.get("date") or "").strip()
            time = (data.get("time") or "").strip()

            if not all([title, date, time]):
                return "❌ Error: Missing required fields for booking (title, date, time)."

            return create_calendar_event(title, date, time)

        elif intent == "query_availability":
            date = (data.get("date") or "").strip()
            time = (data.get("time") or "").strip()

            if not all([date, time]):
                return "❌ Error: Missing fields for availability check (date, time)."

            return check_availability(date, time)

        else:
            return "❌ Error: Could not determine intent (book or query_availability)."

    except json.JSONDecodeError as e:
        return f"❌ Error: Invalid JSON format from Gemini. {str(e)}"
    except Exception as e:
        return f"❌ Error: {str(e)}"
