import os
from dotenv import load_dotenv
from google import genai

# Load API key
load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")

# Create Gemini client
client = genai.Client(api_key=api_key)

MODEL_NAME = "models/gemini-2.5-flash"

print("✅ Gemini chatbot with memory is ready!")
print("Type 'exit' to quit.\n")

# 🧠 Conversation memory
conversation = []

while True:
    user_input = input("You: ")
    if not user_input.strip():
        print("please type something!")
        continue

 
    if user_input.lower() == "exit":
        print("👋 Goodbye!")
        break

    # Add user message to memory
    conversation.append({
        "role": "user",
        "parts": [{"text": user_input}]
    })

    try:
        response = client.models.generate_content(
            model=MODEL_NAME,
            contents=conversation
        )

        bot_reply = response.text
        print("Bot:", bot_reply)

        # Add bot response to memory
        conversation.append({
            "role": "model",
            "parts": [{"text": bot_reply}]
        })

    except Exception as e:
        print("❌ Error:", e)
