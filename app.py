import streamlit as st
import google.generativeai as genai
import os

# API key handling
api_key = st.secrets.get("GEMINI_API_KEY") or os.getenv("GEMINI_API_KEY")

if not api_key:
    st.error("⚠️ Gemini API key not found. Please add it in Streamlit Secrets.")
    st.stop()

genai.configure(api_key=api_key)

# generation config (faster responses)
generation_config = {
    "temperature": 0.4,
    "max_output_tokens": 150
}

# load Gemini 2.5 Flash
model = genai.GenerativeModel(
    "gemini-2.5-flash",
    generation_config=generation_config
)

st.set_page_config(page_title="PromptPilot", page_icon="🤖")

st.title("🤖 PromptPilot")
st.caption("Powered by Google Gemini + Streamlit")

# initialize chat
if "chat" not in st.session_state:
    st.session_state.chat = model.start_chat(history=[])

if "messages" not in st.session_state:
    st.session_state.messages = []

# show chat history
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])

# input layout
col1, col2 = st.columns([5,1])

with col1:
    user_input = st.chat_input("Ask something...")

with col2:
    if st.button("Clear Chat"):
        st.session_state.messages = []
        st.session_state.chat = model.start_chat(history=[])
        st.rerun()

# user message
if user_input:

    with st.chat_message("user"):
        st.write(user_input)

    st.session_state.messages.append({"role": "user", "content": user_input})

    # assistant response
    with st.chat_message("assistant"):
        with st.spinner("Thinking... 🤖"):
            try:
                response = st.session_state.chat.send_message(user_input)
                bot_reply = response.text
            except Exception:
                bot_reply = "⚠️ Error generating response. Please try again."

        st.write(bot_reply)

    st.session_state.messages.append({"role": "assistant", "content": bot_reply})