import streamlit as st
import os
from dotenv import load_dotenv
from groq import Groq

# 1. Setup & Config
load_dotenv()
st.set_page_config(page_title="Elite AI Coach", page_icon="⚡", layout="wide", initial_sidebar_state="expanded")

# --- UI CUSTOMIZATION ---
st.markdown("""
    <style>
        [data-testid="stHeader"] { background-color: rgba(0,0,0,0); }
        .stDeployButton { visibility: hidden; }
        .stApp {
            background: linear-gradient(to bottom right, #0f2027, #203a43, #2c5364);
            color: white;
        }
        .stTextInput > div > div > input {
            background-color: #2c3e50;
            color: white;
            border-radius: 20px;
        }
    </style>
""", unsafe_allow_html=True)

# Initialize Groq
try:
    client = Groq(api_key=os.getenv("GROQ_API_KEY"))
except Exception as e:
    st.error(f"Error connecting to Groq: {e}")

# 2. Initialize Memory
if "history" not in st.session_state:
    st.session_state.history = []

# --- SIDEBAR ---
with st.sidebar:
    st.title("⚙️ Coaching Lab")
    st.markdown("---")
    
    coach_mode = st.selectbox(
        "Choose Your Specialist:",
        ["💼 Business Coach", "💪 Fitness Coach", "🌱 Life Coach", "💰 Finance Coach"]
    )
    
    if st.button("🗑️ Reset Conversation", use_container_width=True):
        st.session_state.history = []
        st.rerun()
        
    st.markdown("---")
    st.info(f"💡 You are now working with your {coach_mode}.")

# 3. Main Interface
st.title(f"⚡ {coach_mode}")

# --- WELCOME LOGIC ---
if not st.session_state.history:
    welcome_messages = {
        "💼 Business Coach": "Welcome to the Boardroom. I'm here to help you scale your vision and dominate your market. What's our first objective?",
        "💪 Fitness Coach": "Welcome to the Lab. We're here to push limits and build a stronger version of you. Ready to crush today's workout?",
        "🌱 Life Coach": "Welcome to your safe space. Let's work on clarity, mindset, and finding your balance. What's on your heart today?",
        "💰 Finance Coach": "Welcome to your Financial Command Center. Let's build your legacy and secure your freedom. Where shall we start?"
    }
    initial_msg = welcome_messages[coach_mode]
    st.session_state.history.append({"role": "assistant", "content": initial_msg})

# 4. Display Chat History
for message in st.session_state.history:
    avatar = "🧑‍💻" if message["role"] == "user" else "🧠"
    with st.chat_message(message["role"], avatar=avatar):
        st.markdown(message["content"])

# 5. Handle Chat Input
if prompt := st.chat_input(f"Message your {coach_mode.lower()}..."):
    with st.chat_message("user", avatar="🧑‍💻"):
        st.markdown(prompt)
    st.session_state.history.append({"role": "user", "content": prompt})

    # --- IMPROVED AI LOGIC FOR GREETINGS ---
    user_input_clean = prompt.lower().strip().strip("!?.")
    
    if user_input_clean in ["hi", "hello", "hey"]:
        # Direct Greeting without calling the API
        greetings = {
            "💼 Business Coach": "Hello! Let's get down to business. What's on the agenda?",
            "💪 Fitness Coach": "Hey! Ready to get to work? Let's crush it.",
            "🌱 Life Coach": "Hello. I'm glad you're here. How can I support you today?",
            "💰 Finance Coach": "Greetings. Ready to review the numbers? Let's begin."
        }
        bot_text = greetings[coach_mode]
        with st.chat_message("assistant", avatar="🧠"):
            st.markdown(bot_text)
        st.session_state.history.append({"role": "assistant", "content": bot_text})
    
    else:
        # Standard API Call for everything else
        try:
            coach_prompts = {
                "💼 Business Coach": "You are a world-class Business Coach. Focus on ROI, market strategy, and scalability.",
                "💪 Fitness Coach": "You are an elite Fitness Coach. Focus on hypertrophy, split routines, and recovery.",
                "🌱 Life Coach": "You are a compassionate Life Coach. Focus on habit formation and mindset.",
                "💰 Finance Coach": "You are a pragmatic Finance Coach. Focus on budgeting and wealth-building."
            }

            system_instruction = {
                "role": "system", 
                "content": f"{coach_prompts[coach_mode]} Keep responses supportive but concise (under 4 sentences)."
            }

            messages_to_send = [system_instruction] + st.session_state.history

            completion = client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=messages_to_send,
                temperature=0.7
            )
            
            bot_text = completion.choices[0].message.content
            with st.chat_message("assistant", avatar="🧠"):
                st.markdown(bot_text)
            st.session_state.history.append({"role": "assistant", "content": bot_text})

        except Exception as e:
            st.error(f"An error occurred: {e}")