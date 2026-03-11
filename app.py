import streamlit as st
import google.generativeai as genai
import os

api_key = st.secrets.get("GEMINI_API_KEY", os.getenv("GEMINI_API_KEY"))
genai.configure(api_key=api_key)

# load model
model = genai.GenerativeModel("gemini-2.5-flash")

st.set_page_config(page_title="Gemini AI Chatbot", page_icon="🤖")

st.title("🤖 PromptPilot")
st.caption("Powered by Google Gemini + Streamlit")

system_prompt = """
You are a helpful AI assistant.
Explain things clearly and simply.
Keep answers short and easy to understand.
"""

# initialize chat
if "chat" not in st.session_state:
    st.session_state.chat = model.start_chat(history=[])

if "messages" not in st.session_state:
    st.session_state.messages = []

# show chat history
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])

# layout for clear button
col1, col2 = st.columns([5,1])

with col1:
    user_input = st.chat_input("Ask something...")

with col2:
    if st.button("Clear Chat"):
        st.session_state.messages = []
        st.session_state.chat = model.start_chat(history=[])
        st.rerun()

# user input
if user_input:

    with st.chat_message("user"):
        st.write(user_input)

    st.session_state.messages.append({"role": "user", "content": user_input})

    response = st.session_state.chat.send_message(system_prompt + user_input)

    bot_reply = response.text

    with st.chat_message("assistant"):
        st.write(bot_reply)

    st.session_state.messages.append({"role": "assistant", "content": bot_reply})