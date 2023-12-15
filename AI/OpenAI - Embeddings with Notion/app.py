# chatbot_app.py
import time
import streamlit as app
from chat_utils import initialize_chatbot_chain

# Streamlit page configuration
app.set_page_config(
    page_title="AI Chatbot for Notion",
    page_icon="https://blendle.com/img/packaging/android-touch-icon-196x196.png",
)

# Set up the chatbot chain
if "chatbot_chain" not in app.session_state:
    app.session_state["chatbot_chain"] = initialize_chatbot_chain()

# Set up chat history
if "chat_history" not in app.session_state:
    app.session_state["chat_history"] = [
        {
            "role": "bot",
            "text": "Greetings! I am the AI assistant from Blendle. How can I assist you?",
        }
    ]

# Display previous chat messages
for msg in app.session_state.chat_history:
    if msg["role"] == "bot":
        with app.chat_message(
            msg["role"],
            avatar="https://blendle.com/img/packaging/android-touch-icon-196x196.png",
        ):
            app.markdown(msg["text"])
    else:
        with app.chat_message(msg["role"]):
            app.markdown(msg["text"])

# Handle chat input
if user_input := app.chat_input("Your question:"):
    app.session_state.chat_history.append({"role": "user", "text": user_input})

    with app.chat_message(
        "bot", avatar="https://blendle.com/img/packaging/android-touch-icon-196x196.png"
    ):
        placeholder = app.empty()
        chat_response = app.session_state["chatbot_chain"]({"question": user_input})[
            "answer"
        ]
        displayed_response = ""

        for word in chat_response.split():
            displayed_response += word + " "
            time.sleep(0.05)
            placeholder.markdown(displayed_response + "▌")
        placeholder.markdown(displayed_response)

    app.session_state.chat_history.append({"role": "bot", "text": chat_response})
