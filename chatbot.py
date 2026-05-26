import streamlit as st
import os
from groq import Groq
from groq import RateLimitError, APIConnectionError

# ===================== PAGE CONFIG =====================
st.set_page_config(
    page_title="Carepod Support",
    page_icon="💧",
    layout="centered"
)

# ===================== CUSTOM CSS =====================
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@300;400;500;600&display=swap');

/* Global dark theme */
html, body, [data-testid="stAppViewContainer"], [data-testid="stApp"] {
    background-color: #111111 !important;
    color: #f5f5f5 !important;
    font-family: 'DM Sans', sans-serif !important;
}

[data-testid="stHeader"] {
    background-color: #111111 !important;
}

/* Hide default streamlit elements */
#MainMenu, footer, header { visibility: hidden; }
[data-testid="stToolbar"] { display: none; }

/* Main container */
[data-testid="stAppViewContainer"] > .main {
    background-color: #111111;
    padding: 0 !important;
}

.block-container {
    padding: 0 !important;
    max-width: 100% !important;
}

/* Top nav bar */
.carepod-nav {
    background: #111111;
    border-bottom: 1px solid #2a2a2a;
    padding: 14px 24px;
    display: flex;
    align-items: center;
    justify-content: space-between;
    position: sticky;
    top: 0;
    z-index: 999;
}

.carepod-logo {
    font-family: 'DM Sans', sans-serif;
    font-size: 18px;
    font-weight: 600;
    color: #ffffff;
    letter-spacing: 0.08em;
    text-transform: uppercase;
}

.nav-links {
    display: flex;
    gap: 24px;
}

.nav-link {
    font-size: 13px;
    color: #888888;
    text-decoration: none;
    letter-spacing: 0.03em;
}

/* Chat container — blue card like the website */
.chat-widget {
    background: #1a6af5;
    border-radius: 16px;
    padding: 0;
    margin: 24px auto;
    max-width: 480px;
    overflow: hidden;
    box-shadow: 0 8px 40px rgba(26,106,245,0.25);
}

.chat-header {
    background: #1a6af5;
    padding: 20px 20px 14px;
    border-bottom: 1px solid rgba(255,255,255,0.12);
}

.chat-header-logo {
    font-size: 16px;
    font-weight: 700;
    color: #ffffff;
    letter-spacing: 0.1em;
    text-transform: uppercase;
    margin-bottom: 6px;
}

.chat-header-sub {
    font-size: 12px;
    color: rgba(255,255,255,0.65);
    line-height: 1.5;
}

/* Chat messages area */
[data-testid="stChatMessageContainer"] {
    background: #f9f9f7 !important;
    padding: 16px !important;
    border-radius: 0 !important;
    min-height: 300px;
}

/* User messages */
[data-testid="stChatMessage"][data-role="user"] {
    background: #1a6af5 !important;
    color: white !important;
    border-radius: 18px 18px 4px 18px !important;
    padding: 10px 14px !important;
    margin-left: auto !important;
    max-width: 80% !important;
    margin-bottom: 10px !important;
}

[data-testid="stChatMessage"][data-role="user"] p {
    color: white !important;
}

/* Assistant messages */
[data-testid="stChatMessage"][data-role="assistant"] {
    background: #ffffff !important;
    color: #111111 !important;
    border-radius: 18px 18px 18px 4px !important;
    padding: 10px 14px !important;
    max-width: 80% !important;
    margin-bottom: 10px !important;
    border: 1px solid #e8e8e8 !important;
}

[data-testid="stChatMessage"][data-role="assistant"] p {
    color: #111111 !important;
}

/* Hide avatar icons */
[data-testid="stChatMessageAvatarUser"],
[data-testid="stChatMessageAvatarAssistant"] {
    display: none !important;
}

/* Chat input */
[data-testid="stChatInput"] {
    background: #ffffff !important;
    border-top: 1px solid #e8e8e8 !important;
    padding: 12px 16px !important;
    border-radius: 0 0 16px 16px !important;
}

[data-testid="stChatInputContainer"] {
    background: #f3f3f0 !important;
    border-radius: 24px !important;
    border: none !important;
}

[data-testid="stChatInputContainer"] textarea {
    background: transparent !important;
    color: #111111 !important;
    font-family: 'DM Sans', sans-serif !important;
    font-size: 14px !important;
}

[data-testid="stChatInputContainer"] textarea::placeholder {
    color: #888888 !important;
}

/* Spinner */
[data-testid="stSpinner"] {
    color: #1a6af5 !important;
}

/* Banner */
.carepod-banner {
    background: #1a6af5;
    padding: 10px 24px;
    text-align: center;
    font-size: 13px;
    color: rgba(255,255,255,0.85);
    font-weight: 400;
    letter-spacing: 0.02em;
}

.carepod-banner a {
    color: #ffffff;
    font-weight: 600;
    text-decoration: underline;
}

/* Quick action pills */
.quick-actions {
    display: flex;
    flex-wrap: wrap;
    gap: 8px;
    padding: 12px 16px 16px;
    background: #f9f9f7;
}

.quick-pill {
    background: #ffffff;
    border: 1px solid #e0e0dc;
    border-radius: 20px;
    padding: 7px 14px;
    font-size: 13px;
    color: #333333;
    cursor: pointer;
    font-family: 'DM Sans', sans-serif;
    transition: all 0.15s ease;
}

.quick-pill:hover {
    background: #1a6af5;
    color: #ffffff;
    border-color: #1a6af5;
}

/* Footer note */
.chat-footer-note {
    font-size: 11px;
    color: rgba(255,255,255,0.5);
    text-align: center;
    padding: 8px 16px 12px;
    background: #1a6af5;
    border-top: 1px solid rgba(255,255,255,0.1);
}
</style>
""", unsafe_allow_html=True)

# ===================== TOP BANNER =====================
st.markdown("""
<div class="carepod-banner">
    Free Shipping & Returns &nbsp;|&nbsp; <a href="https://hellocarepod.com" target="_blank">Shop Carepod</a>
</div>
""", unsafe_allow_html=True)

# ===================== NAV =====================
st.markdown("""
<div class="carepod-nav">
    <div class="carepod-logo">✦ Carepod</div>
    <div class="nav-links">
        <a class="nav-link" href="https://hellocarepod.com/pages/faqs" target="_blank">FAQ</a>
        <a class="nav-link" href="https://support.hellocarepod.com" target="_blank">Support</a>
        <a class="nav-link" href="https://hellocarepod.com/pages/contact-us" target="_blank">Contact</a>
    </div>
</div>
""", unsafe_allow_html=True)

# ===================== CHAT HEADER =====================
st.markdown("""
<div style="max-width:480px; margin: 24px auto 0;">
    <div style="background:#1a6af5; border-radius:16px 16px 0 0; padding:20px 20px 14px; border-bottom:1px solid rgba(255,255,255,0.12);">
        <div style="font-size:16px; font-weight:700; color:#fff; letter-spacing:0.08em; text-transform:uppercase; margin-bottom:4px;">✦ CAREPOD</div>
        <div style="font-size:12px; color:rgba(255,255,255,0.65); line-height:1.5;">
            This chat is AI-powered for faster assistance.<br>
            <a href="https://hellocarepod.com/pages/contact-us" style="color:rgba(255,255,255,0.85);" target="_blank">Connect with a specialist →</a>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

# ===================== API SETUP =====================
GROQ_API_KEY = st.secrets.get("GROQ_API_KEY") or os.getenv("GROQ_API_KEY")

if not GROQ_API_KEY:
    st.error("Please add your Groq API Key in Streamlit secrets.")
    st.stop()

client = Groq(api_key=GROQ_API_KEY)

# ===================== SYSTEM PROMPT =====================
system_prompt = """
You are Nova, the official AI Customer Support Assistant for Carepod — a premium humidifier brand known for elegant design, easy cleaning, and high-quality oscillating technology.

Tone: Professional, friendly, calm, empathetic, and solution-oriented.

Core Rules:
- Keep responses short and concise (2-5 sentences or bullet points max).
- Always be polite and empathetic.
- Never guess or fabricate information.
- Always ask for Order Number when discussing warranty, returns, or replacements.
- Offer to connect with a human specialist for refunds or replacements.
- Direct users to support@hellocarepod.com or https://hellocarepod.com/pages/contact-us for unresolved issues.
- Support hours: Monday–Friday, 9am–5pm CST.

Product Lineup:
- Carepod Cube Plus — up to 700 sq ft
- Carepod One Plus — up to 500 sq ft
- Carepod One Plus With Stand — up to 500 sq ft
- Carepod One — up to 500 sq ft
- Carepod Mini — up to 350 sq ft (great for nurseries)

Official Policies:
- 1-year Manufacturer's Warranty on main body (water tank, silicone seal, airguard cover, inner lid cover, power cord)
- 2-year Manufacturer's Warranty on the white oscillating wand
- Warranty claims: https://returns.hellocarepod.com/warranty/shopify
- Warranty registration: https://support.hellocarepod.com/register

Water Guidelines:
- Always use distilled or filtered water
- Tap water causes mineral buildup, white dust, and wand damage

Cleaning Instructions:
- Remove 3 parts: water tank, inner lid cover, white wand
- Handwash water tank and inner lid cover with dish soap; may sterilize in boiling water
- Wash ONLY the bottom half of the white wand with mild soap and soft sponge/toothbrush
- To sterilize the wand: dip the base in boiling water for 1-2 seconds ONLY
- Dry all parts fully with a clean towel
- Clean at least once a week

Common Issues & Solutions:

1. Won't turn on:
   - Check power cord is fully plugged in
   - Try a different outlet
   - Inspect white wand for water or damage

2. Black spots / residue on wand:
   - Caused by mineral deposits from tap water
   - Clean bottom half of wand with soft sponge
   - Dip base in boiling water for 1-2 seconds to sterilize
   - Switch to distilled or filtered water

3. Water accumulating under tank:
   - Check water tank lip is aligned with main body
   - Push inner lid cover fully using the white knob
   - Press edges of silicone seal to ensure it's fully seated

4. Mist collecting on floor:
   - Place Carepod at least 2 feet off the floor
   - Set mist intensity to Low (Level 1)
   - Use timer feature (4–8 hours)

5. Dripping sound:
   - Completely normal — water condensation falling from inner lid into tank

6. Lights won't turn off:
   - Cube Plus and One Plus have Night/Dark Mode
   - Tap and hold button for 2 seconds to activate
   - Tap any button to exit Night/Dark mode

7. Sanitization (Cube Plus only):
   - Press and hold Heater/Sanitize button until beep
   - Left LED turns solid white, right LED blinks red = scheduled
   - Water may reach 158°F–167°F during cycle — use caution

Response Structure:
1. Acknowledge the issue briefly with empathy.
2. Ask for missing details if needed (Order Number, model, symptoms).
3. Provide short, clear solution (max 3-4 steps).
4. End with next steps or offer further help.
"""

# ===================== CHAT HISTORY =====================
if "messages" not in st.session_state:
    st.session_state.messages = []

# Wrap messages in the chat widget body
st.markdown('<div style="max-width:480px; margin: 0 auto;">', unsafe_allow_html=True)
st.markdown('<div style="background:#f9f9f7; min-height:300px; padding:16px;">', unsafe_allow_html=True)

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

st.markdown('</div>', unsafe_allow_html=True)

# Quick action pills (only show if no messages yet)
if not st.session_state.messages:
    st.markdown("""
    <div style="background:#f9f9f7; padding: 4px 16px 16px; display:flex; flex-wrap:wrap; gap:8px;">
        <span style="background:#fff; border:1px solid #e0e0dc; border-radius:20px; padding:7px 14px; font-size:13px; color:#333; font-family:'DM Sans',sans-serif; cursor:pointer;">🔧 Wand not working</span>
        <span style="background:#fff; border:1px solid #e0e0dc; border-radius:20px; padding:7px 14px; font-size:13px; color:#333; font-family:'DM Sans',sans-serif; cursor:pointer;">📦 Track my order</span>
        <span style="background:#fff; border:1px solid #e0e0dc; border-radius:20px; padding:7px 14px; font-size:13px; color:#333; font-family:'DM Sans',sans-serif; cursor:pointer;">🛡️ Warranty info</span>
        <span style="background:#fff; border:1px solid #e0e0dc; border-radius:20px; padding:7px 14px; font-size:13px; color:#333; font-family:'DM Sans',sans-serif; cursor:pointer;">🧹 How to clean</span>
    </div>
    """, unsafe_allow_html=True)

# Chat input
if prompt := st.chat_input("Ask anything about your Carepod..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        with st.spinner(""):
            try:
                history = [{"role": "system", "content": system_prompt}]
                for m in st.session_state.messages:
                    history.append({"role": m["role"], "content": m["content"]})

                response = client.chat.completions.create(
                    model="llama-3.3-70b-versatile",
                    messages=history,
                    max_tokens=300
                )
                response_text = response.choices[0].message.content

            except RateLimitError:
                response_text = "⚠️ Too many requests. Please wait a moment and try again."
            except APIConnectionError:
                response_text = "⚠️ Connection error. Please check your internet and try again."
            except Exception:
                response_text = "⚠️ Something went wrong. Please try again in a moment."

            st.markdown(response_text)
            st.session_state.messages.append({"role": "assistant", "content": response_text})

# Footer note
st.markdown("""
<div style="background:#1a6af5; border-top:1px solid rgba(255,255,255,0.1); border-radius:0 0 16px 16px; padding:10px 16px; text-align:center; font-size:11px; color:rgba(255,255,255,0.55); max-width:480px; margin:0 auto;">
    This chat may be monitored for quality. &nbsp;·&nbsp; 
    <a href="https://hellocarepod.com/policies/privacy-policy" style="color:rgba(255,255,255,0.75);" target="_blank">Privacy Policy</a>
</div>
""", unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)
