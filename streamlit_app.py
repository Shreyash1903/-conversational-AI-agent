import streamlit as st
import requests

# -------------- Page Config ------------------
st.set_page_config(page_title="AI Booking Assistant", page_icon="📅", layout="wide")

# -------------- Font, Button, and Theme Styling ------------------
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Montserrat:wght@400;600&display=swap');

    html, body, [class*="css"] {
        font-family: 'Montserrat', sans-serif !important;
    }

    h1, h2, h3, h4, h5, h6, div, p, span, input, label, textarea, button {
        font-family: 'Montserrat', sans-serif !important;
    }

    .user-bubble {
        background-color: #DCF8C6;
        padding: 10px 15px;
        border-radius: 15px;
        margin: 8px 0;
        max-width: 80%;
        align-self: flex-end;
        text-align: right;
    }

    .bot-bubble {
        background-color: #F1F0F0;
        padding: 10px 15px;
        border-radius: 15px;
        margin: 8px 0;
        max-width: 80%;
        align-self: flex-start;
        text-align: left;
    }

    .chat-container {
        display: flex;
        flex-direction: column;
    }

    label, .stTextInput label {
        color: black !important;
    }

    .dark label, .dark .stTextInput label {
        color: white !important;
    }

    .dark .stTextInput input {
        background-color: #1e1e1e !important;
        color: white !important;
    }

    input::placeholder {
        color: #bbbbbb !important;
    }

    /* Button Styling */
    div.stButton > button {
        background-color: #4B8BBE;
        color: white;
        border: none;
        padding: 0.6em 1.2em;
        border-radius: 6px;
        font-weight: 600;
        transition: transform 0.2s ease, box-shadow 0.2s ease;
    }

    div.stButton > button:hover {
        transform: scale(1.03);
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.2);
        color: white !important;
    }

    div.stButton > button:active {
        background-color: #4B8BBE !important;
        color: white !important;
        transform: scale(1.01);
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
    }

    /* 🔒 REMOVE red or blue outlines on focus/click */
    div.stButton > button:focus,
    div.stButton > button:focus-visible,
    div.stButton > button:active:focus,
    div.stButton > button:focus-within {
        outline: none !important;
        box-shadow: none !important;
        background-color: #4B8BBE !important;
        color: white !important;
    }
    </style>
""", unsafe_allow_html=True)

# -------------- Sidebar Dashboard ------------------
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/2922/2922510.png", width=100)
    st.markdown("## 👋 Welcome, Shreyash")
    st.markdown("AI Calendar Assistant")

    # Theme Switch
    theme = st.radio("🌓 Theme", ["Light", "Dark"], index=0)
    if theme == "Dark":
        st.markdown("""
            <style>
            .stApp {
                background-color: #0e1117 !important;
                color: white !important;
            }
            .sidebar .sidebar-content {
                background-color: #0e1117 !important;
            }
            </style>
        """, unsafe_allow_html=True)
        st.markdown("""
            <script>
            document.documentElement.classList.add("dark");
            </script>
        """, unsafe_allow_html=True)

    st.markdown("---")

    # Quick test prompts
    st.markdown("### 🧪 Quick Test")
    test_prompt = st.selectbox("Choose a test prompt", [
        "Schedule meeting tomorrow at 3 PM",
        "Am I free next Monday at 10 AM?",
        "Book a catch-up Friday 5 PM",
        "Schedule something at noon",
        "Random text"
    ])

    if st.button("▶️ Run Test Case"):
        st.session_state.user_input = test_prompt

    st.markdown("---")
    st.markdown("Made with ❤️ using Streamlit")

# -------------- Chat State ------------------
if "messages" not in st.session_state:
    st.session_state.messages = []

# -------------- Title & Description ------------------
st.title("📅 SmartCalendarBot")

st.markdown("""
<div style="background-color:#f0f2f6; padding: 20px; border-radius: 10px; margin-bottom: 20px;">
    <h4 style="color:#4B8BBE; margin-top: 0;">AI-Driven Conversational Booking Assistant with Google Calendar Integration</h4>
    <p style="font-size:16px; color:#333333;">
        SmartCalendarBot enables users to book appointments effortlessly through a human-like chat interface.
        The bot interprets user queries using NLP, checks real-time calendar availability,
        and handles conflicts or preferences, making scheduling fast and frictionless.
    </p>
</div>
""", unsafe_allow_html=True)

st.subheader("Schedule Meetings with Natural Language !")

# -------------- Chat History ------------------
st.markdown('<div class="chat-container">', unsafe_allow_html=True)
for msg in st.session_state.messages:
    bubble_class = "user-bubble" if msg["role"] == "user" else "bot-bubble"
    st.markdown(f'<div class="{bubble_class}">{msg["content"]}</div>', unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)

# -------------- User Input Field ------------------
user_input = st.text_input(
    "What would you like to schedule ?",
    value=st.session_state.get("user_input", ""),
    placeholder="e.g., Schedule a Meeting this Friday at 2 PM"
)

# -------------- Send Button Logic ------------------
if st.button("🚀 Schedule Meeting"):
    if not user_input.strip():
        st.warning("Please enter something.")
    else:
        try:
            st.session_state.messages.append({"role": "user", "content": user_input})

            response = requests.post("http://localhost:8000/chat", json={"user_input": user_input})
            data = response.json()
            message = data.get("response", "No response.")
            parsed = data.get("parsed", {})

            st.session_state.messages.append({"role": "bot", "content": message})
            st.success(message)

            if "You are free" in message and parsed:
                if st.button("📌 Want to book this meeting?"):
                    parsed["intent"] = "book"
                    response = requests.post("http://localhost:8000/chat", json={"user_input": str(parsed)})
                    final_msg = response.json().get("response", "Meeting booked!")
                    st.success(final_msg)
                    st.session_state.messages.append({"role": "bot", "content": final_msg})

        except requests.exceptions.ConnectionError:
            st.error("❌ Backend server is not running (localhost:8000).")
        except Exception as e:
            st.error(f"❌ Unexpected error: {str(e)}")
