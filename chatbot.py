import streamlit as st
import os
from groq import Groq
from groq import RateLimitError, APIConnectionError

# ===================== CONFIG =====================
st.set_page_config(page_title="Carepod AI Support", page_icon="💧", layout="centered")
st.title("💧 Carepod AI Customer Support")
st.markdown("**Official AI Assistant** — Get help with your humidifier")

GROQ_API_KEY = st.secrets.get("GROQ_API_KEY") or os.getenv("GROQ_API_KEY")

if not GROQ_API_KEY:
    st.error("Please add your Groq API Key in Streamlit secrets.")
    st.stop()

client = Groq(api_key=GROQ_API_KEY)

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
                # Build full conversation history
                history = [{"role": "system", "content": system_prompt}]
                for m in st.session_state.messages:
                    history.append({"role": m["role"], "content": m["content"]})

                response = client.chat.completions.create(
                    model="llama-3.3-70b-versatile",  # Free & powerful
                    messages=history,
                    max_tokens=1000
                )
                response_text = response.choices[0].message.content

            except RateLimitError:
                response_text = "⚠️ Too many requests. Please wait a moment and try again."
            except APIConnectionError:
                response_text = "⚠️ Connection error. Please check your internet and try again."
            except Exception as e:
                response_text = "⚠️ Something went wrong. Please try again in a moment."

            st.markdown(response_text)
            st.session_state.messages.append({"role": "assistant", "content": response_text})
