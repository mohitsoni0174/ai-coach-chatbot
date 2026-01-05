import streamlit as st
import os
from dotenv import load_dotenv
from groq import Groq

# 1. Load the secret key securely
load_dotenv()
api_key = os.getenv("GROQ_API_KEY")

# 2. Setup the Page
st.set_page_config(page_title="AI Coach", page_icon="⚡")
st.title("⚡ My AI Coach (Powered by Groq)")

# 3. Check for Key
if not api_key:
    st.error("❌ API Key not found! Please check your .env file.")
    st.stop()

# 4. Initialize the Groq Client
client = Groq(api_key=api_key)

# 5. Initialize Chat History
if "messages" not in st.session_state:
    st.session_state.messages = []

# 6. Display Chat History
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# 7. Handle User Input
if prompt := st.chat_input("Ask your coach something..."):
    # Add user message to history
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Generate Response
    with st.chat_message("assistant"):
        stream = client.chat.completions.create(
            messages=[
                # System prompt to define the coach's personality
                {
                    "role": "system",
                    "content": "You are a helpful, no-nonsense AI coach. Keep answers concise and actionable."
                }
            ] + st.session_state.messages, # Add conversation history
            
            # The Model (Llama 3 is fast and free on Groq)
            model="llama-3.3-70b-versatile", 
            
            # Streaming for fast "typing" effect
            stream=True,
        )
        
        # Display the response as it types
        response = st.write_stream(stream)
    
    # Add assistant response to history
    st.session_state.messages.append({"role": "assistant", "content": response})