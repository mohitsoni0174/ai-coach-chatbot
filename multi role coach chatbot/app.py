import streamlit as st
import os
from dotenv import load_dotenv
from groq import Groq

# 1. Setup & Config
load_dotenv()
st.set_page_config(page_title="My AI COACH", page_icon="🤖")
st.title("🤖 My Coach")
# --- UI Customization ---
st.markdown("""
    <style>
        /* 1. Hide the Streamlit Header & Footer */
        header {visibility: hidden;}
        .stApp footer {display: none;}
        
        /* 2. Main Background Gradient */
        .stApp {
            background: linear-gradient(to bottom right, #0f2027, #203a43, #2c5364);
            color: white;
        }
        
        /* 3. Style the Text Input Box */
        .stTextInput > div > div > input {
            background-color: #2c3e50;
            color: white;
            border-radius: 20px;
        }
    </style>
""", unsafe_allow_html=True)
# --- UI CUSTOMIZATION END ---

# Initialize the Client
try:
    client = Groq(api_key=os.getenv("GROQ_API_KEY"))
except Exception as e:
    st.error(f"Error connecting to Groq: {e}")

# 2. Initialize Memory
if "history" not in st.session_state:
    st.session_state.history = []

# 3. Display Previous Chats
for message in st.session_state.history:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# 4. The Input Box
prompt = st.chat_input("Type a message...")

if prompt:
    # A. Display User Message
    with st.chat_message("user"):
        st.markdown(prompt)
    
    # B. Add to History (Groq Format: simple 'content', not 'parts')
    st.session_state.history.append({"role": "user", "content": prompt})

    # C. Get Response
    try:
        # Define the personality (System Prompt)
        system_instruction = {
            "role": "system", 
            "content": """
           You are an expert AI Life Coach.
            Your Goal: Help the user achieve clarity, solve problems, and take action.
            
            Guidelines:
            1. Be encouraging but direct. Don't just chat—drive the conversation forward.
            2. When the user asks for help, use clear steps or bullet points.
            3. When the user says "Hi", welcome them warmly as their coach.
            4. Keep responses concise (under 3-4 sentences) unless explaining a complex plan.
            """
        }

        # Combine System Prompt + History
        messages = [system_instruction] + st.session_state.history

        # Call Groq API
        completion = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=messages,
            temperature=0.7
        )
        
        # Extract Text
        bot_text = completion.choices[0].message.content

        # D. Display & Save Bot Response
        with st.chat_message("assistant"):
            st.markdown(bot_text)
            
        st.session_state.history.append({"role": "assistant", "content": bot_text})

    except Exception as e:
        st.error(f"An error occurred: {e}")