import streamlit as st
import google.generativeai as genai
import os
from google.api_core.exceptions import ResourceExhausted, NotFound, InvalidArgument

# ===================== CONFIG =====================
st.set_page_config(page_title="Carepod AI Support", page_icon="💧", layout="centered")
st.title("💧 Carepod AI Customer Support")
st.markdown("**Official AI Assistant** — Get help with your humidifier")

GEMINI_API_KEY = st.secrets.get("GEMINI_API_KEY") or os.getenv("GEMINI_API_KEY")

if not GEMINI_API_KEY:
    st.error("Please add your Gemini API Key in the sidebar.")
    with st.sidebar:
        api_key = st.text_input("Enter Gemini API Key:", type="password")
        if st.button("Save Key"):
            st.session_state.api_key = api_key
            st.success("Key saved!")
    st.stop()

genai.configure(api_key=GEMINI_API_KEY)

# ===================== SYSTEM PROMPT =====================
system_prompt = """
You are Nova, the official AI Customer Support Assistant for Carepod — a premium humidifier brand.
Tone: Professional, friendly, calm, empathetic, and solution-oriented.
Core Rules:
- Always be polite and empathetic.
- Use bullet points and numbered steps for instructions.
- Official Policies: 30-day return | 1-year warranty on main unit | 2-year warranty on white oscillating wand.
- Strongly recommend distilled or filtered water.
- Always ask for Order Number when discussing warranty, returns, or replacements.
- Never guess information.
Response Structure (Follow exactly):
1. Acknowledge the issue with empathy.
2. Ask for missing details if needed (Order #, model, symptoms).
3. Provide clear step-by-step solution.
4. End with next steps and offer more help.
"""

# ===================== CHAT HISTORY =====================
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# ===================== CHAT INPUT =====================
if prompt := st.chat_input("Ask me anything about your Carepod humidifier..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            try:
                model = genai.GenerativeModel(
                    model_name="gemini-2.0-flash-lite",
                    system_instruction=system_prompt
                )

                # Build full conversation history for context
                history = [
                    {"role": m["role"], "parts": [m["content"]]}
                    for m in st.session_state.messages
                ]

                response = model.generate_content(history)
                response_text = response.text

            except ResourceExhausted:
                response_text = "⚠️ I'm receiving too many requests right now. Please wait a moment and try again."

            except NotFound:
                response_text = "⚠️ There was an issue connecting to the AI model. Please contact support."

            except InvalidArgument:
                response_text = "⚠️ There was a problem with the request. Please try rephrasing your message."

            except Exception as e:
                response_text = "⚠️ Something went wrong on my end. Please try again in a moment."

            st.markdown(response_text)
            st.session_state.messages.append({"role": "assistant", "content": response_text})
