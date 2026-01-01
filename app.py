import streamlit as st
import os
from google import genai
from dotenv import load_dotenv

# 1. Setup & Config
load_dotenv()
st.set_page_config(page_title="My AI Chatbot", page_icon="🤖")
st.title("🤖 My Gemini Assistant")

# Initialize the Client
# (Make sure your .env file is in the same folder!)
try:
    client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))
except Exception as e:
    st.error(f"Error connecting to Google: {e}")

# 2. Initialize Memory (Session State)
# Streamlit refreshes the code every time you click a button.
# We need 'session_state' to keep the memory alive between refreshes.
if "history" not in st.session_state:
    st.session_state.history = []

# 3. Display Previous Chats
# We loop through the memory and draw the messages on screen
for message in st.session_state.history:
    role = message["role"]
    text = message["parts"][0]["text"]
    
    # Translate "model" to "assistant" for Streamlit's icon system
    display_role = "assistant" if role == "model" else "user"
    
    with st.chat_message(display_role):
        st.markdown(text)

# 4. The Input Box
# This replaces 'input("You: ")'. It creates a chat box at the bottom.
prompt = st.chat_input("Type a message...")

if prompt:
    # A. Display User Message Immediately
    with st.chat_message("user"):
        st.markdown(prompt)
    
    # B. Save User Message to History (Manual Way)
    user_message = {"role": "user", "parts": [{"text": prompt}]}
    st.session_state.history.append(user_message)

    # C. Get Response from Google
    try:
        # We send the ENTIRE history (st.session_state.history)
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=st.session_state.history,
            config={
            # This is the "Brain Implant" for Coaching
            "system_instruction": """
                You are a pragmatic AI Coach focused on clear logic and reliability. 
                Your goal is to help the user solve problems without over-engineering.
                
                Follow these rules for every response:
                1. STRUCTURE: Use bullet points or numbered lists. Avoid walls of text.
                2. LOGIC: Explain the 'Why' before the 'How'. Use First Principles thinking.
                3. TONE: Be direct, encouraging, and professional. No fluff.
                4. RELIABILITY: If you don't know something, admit it immediately. Do not guess.
            """
        }
        )
        bot_text = response.text

        # D. Display Bot Response
        with st.chat_message("assistant"):
            st.markdown(bot_text)
            
        # E. Save Bot Response to History (Manual Way)
        bot_message = {"role": "model", "parts": [{"text": bot_text}]}
        st.session_state.history.append(bot_message)

    except Exception as e:
        st.error(f"An error occurred: {e}")