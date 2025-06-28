# Conversational AI Agent

Build a conversational AI agent that can assist users in booking appointments on your Google Calendar. The agent should be capable of engaging in a natural, back-and-forth conversation with the user, understanding their intent, checking calendar availability, suggesting suitable time slots, and confirming bookings — all seamlessly through chat.

## Setup Instructions

### 1. Clone the Repository
```bash
git clone https://github.com/Shreyash1903/-conversational-AI-agent.git
cd calendar_bot_project
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Google Calendar API Setup

#### Create Google Cloud Project and Enable Calendar API
1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create a new project or select an existing one
3. Enable the Google Calendar API
4. Create OAuth 2.0 credentials

#### Configure Credentials
1. Copy `credentials.json.template` to `credentials.json`
2. Fill in your Google OAuth credentials from the Cloud Console
3. The first time you run the app, it will open a browser to authenticate and create `app/token.json`

### 4. Run the Application

#### Streamlit Web Interface
```bash
streamlit run streamlit_app.py
```

#### Command Line Interface
```bash
python app/main.py
```

## Security Note

- `credentials.json` and `app/token.json` contain sensitive OAuth credentials
- These files are excluded from git via `.gitignore`
- Use the template files as reference for the required structure
- Never commit actual credential files to version control
