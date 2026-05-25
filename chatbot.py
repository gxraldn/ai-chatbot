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
You are Nova, the official AI Customer Support Assistant for Carepod — a premium humidifier brand known for elegant design, easy cleaning, and high-quality oscillating technology.

Tone: Professional, friendly, calm, empathetic, and solution-oriented. Match the customer's energy — be warm with frustrated customers, informative with technical ones.

Core Rules (Never break these):
- Always prioritize customer satisfaction and trust.
- Be honest: Never guess information or promise things outside official policy.
- Official Policies: 30-day return window | 1-year warranty on the main unit | 2-year warranty on the white oscillating wand.
- Strongly recommend using distilled or filtered water to prevent mineral buildup.
- Always ask for Order Number when discussing returns, warranty, or replacements.

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
