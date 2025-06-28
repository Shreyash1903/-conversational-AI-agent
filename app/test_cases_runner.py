import requests
import json

API_URL = "http://localhost:8000/chat"

# Define all test prompts and expected keywords
test_cases = [
    {
        "prompt": "Schedule a team sync tomorrow at 3 PM",
        "expect": "Meeting scheduled"
    },
    {
        "prompt": "Am I free next Friday at 2 PM?",
        "expect": "You are free"
    },
    {
        "prompt": "Book a discussion next Monday at 10 AM",
        "expect": "Meeting scheduled"
    },
    {
        "prompt": "Can I schedule something at 11 AM tomorrow?",
        "expect": "Missing required fields"
    },
    {
        "prompt": "Schedule catch-up today at 9 AM",  # assuming time is already past 9 AM
        "expect": "Cannot book a meeting in the past"
    },
    {
        "prompt": "Do I have time on Sunday at 5 PM?",
        "expect": "free"
    },
    {
        "prompt": "Book sync tomorrow at 11 AM",  # simulate already booked time
        "expect": "already have a meeting"
    },
    {
        "prompt": "Meeting tomorrow",
        "expect": "Missing required fields"
    },
    {
        "prompt": "Catch-up with John later in the week",
        "expect": "Meeting scheduled"  # depending on Gemini output
    },
    {
        "prompt": "Schedule call tomorrow at 12 AM",
        "expect": "Meeting scheduled"
    },
    {
        "prompt": "Schedule catch-up tomorrow at noon",
        "expect": "Meeting scheduled"
    },
    {
        "prompt": "Blah bleh bloh boop",
        "expect": "Could not determine intent"
    },
]

print("🧪 Running Test Cases...\n")

for i, test in enumerate(test_cases, start=1):
    print(f"Test {i}: {test['prompt']}")
    try:
        response = requests.post(API_URL, json={"user_input": test["prompt"]})
        data = response.json()
        output = data.get("response", "No response received")
        print("Response:", output)

        if test["expect"].lower() in output.lower():
            print("✅ Passed\n")
        else:
            print("❌ Failed\n")
    except Exception as e:
        print("❌ Error while testing:", str(e), "\n")
