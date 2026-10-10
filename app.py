import streamlit as st
from groq import Groq
import os
import requests
import urllib.parse
from bs4 import BeautifulSoup

# 1. Page Configuration (Wide Mode)
st.set_page_config(page_title="AG ChatGPT Plus", page_icon="🧠", layout="wide")

st.markdown("""
<style>
    .reportview-container { background: #1e1e2e; }
    h1 { color: #1f8fff; font-weight: 700; }
    .stChatMessage { border-radius: 10px; margin-bottom: 10px; }
    .block-container { padding-bottom: 150px; }
</style>
""", unsafe_allow_html=True)

st.title("🧠 AG ChatGPT Plus - Executive AI")
st.caption("2026 Enterprise Network: Active Neural Chat Platform")

# Secure Token Configuration
GROQ_API_KEY = os.environ.get("GROQ_API_KEY", "") 
GROQ_MODEL = os.environ.get("GROQ_MODEL", "llama-3.3-70b")

if not GROQ_API_KEY:
    st.error("❌ GROQ_API_KEY नहीं मिली! कृपया इसे अपने Environment Variables या Streamlit Secrets में सेट करें।")
    st.stop()

client = Groq(api_key=GROQ_API_KEY)

# Session States Initializing
if "messages" not in st.session_state:
    st.session_state.messages = []

# पुराना चैट इतिहास स्क्रीन पर बनाए रखने के लिए लूप
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# 2. 📂 SIDEBAR: Control Panel (सिर्फ साफ़ जानकारी के लिए)
with st.sidebar:
    st.header("📂 ChatGPT Control Panel")
    st.info("Directly input prompts, clear text history, and chat in real-time.")
    
    # चैट इतिहास साफ़ करने का बटन ताकि मेमोरी फ्रेश की जा सके
    if st.button("🗑️ Clear Chat History", use_container_width=True):
        st.session_state.messages = []
        st.rerun()

# 3. 🌐 लाइव वेब हब क्रॉलर फंक्शन
def fetch_global_and_social_search(query_text):
    context = ""
    try:
        encoded_query = urllib.parse.quote(query_text)
        search_url = f"https://duckduckgo.com"
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36',
            'Content-Type': 'application/x-www-form-urlencoded'
        }
        data = {'q': query_text}
        
        search_response = requests.post(search_url, headers=headers, data=data, timeout=8)
        if search_response.status_code == 200:
            soup = BeautifulSoup(search_response.text, 'html.parser')
            tds = soup.find_all('td', class_='result-snippet')
            web_data = [td.text.strip() for td in tds[:4] if td.text.strip()]
            if web_data:
                context = "\n".join([f"- Real-time Live Fact: {d}" for d in web_data])
    except Exception:
        pass
    return context

# 4. 💬 MAIN CHAT BOX FLOW
user_input = st.chat_input("Search anything, ask questions, explore real-time trends...")

if user_input:
    # 1. यूजर का मैसेज तुरंत लिस्ट में डालें और स्क्रीन पर दिखाएं
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.markdown(user_input)
        
    # 2. असिस्टेंट का रिस्पॉन्स ब्लॉक शुरू करें
    with st.chat_message("assistant"):
        with st.spinner("🔍 Deep searching live internet servers..."):
            web_context = fetch_global_and_social_search(user_input)
            
            # बिल्कुल सटीक और छोटा जवाब देने के नियम के साथ सिस्टम प्रॉम्ट
            system_prompt = (
                "You are AG ChatGPT Plus, a world-class autonomous AI collaborator. "
                "Today's date is verified as Saturday, October 10, 2026. Current West Bengal CM is Suvendu Adhikari since May 2026.\n\n"
                "CRITICAL RESPONSE RULE: Be extremely direct, concise, and to-the-point. Do NOT provide background history, geography, old context, or long descriptions. Answer ONLY exactly what the user asks for in the minimum possible words.\n\n"
                "CONTEXT AWARENESS: Analyze the conversation history carefully to understand pronouns or related subsequent queries smoothly.\n\n"
                "LIVE DATA DOMINANCE OVERRIDE: You MUST strictly believe the real-time internet data provided below. Ignore your training cut-off completely and use the new live information immediately."
            )
            if web_context:
                system_prompt += f"\n\n[UNIVERSAL LIVE WEB PIPELINE DATA (2026):]\n{web_context}"
            
            # सिस्टम प्रॉम्प्ट के साथ पूरा चैट इतिहास तैयार करें
            api_messages = [{"role": "system", "content": system_prompt}]
            for msg in st.session_state.messages:
                api_messages.append({"role": msg["role"], "content": msg["content"]})
                
            try:
                # Groq API कॉल (choices[0] इंडेक्स एरर को पूरी तरह फिक्स कर दिया गया है)
                completion = client.chat.completions.create(
                    model=GROQ_MODEL,
                    messages=api_messages,
                    stream=False
                )
                full_response = completion.choices[0].message.content
                
                # स्क्रीन पर रेंडर करें और मेमोरी में सुरक्षित सेव करें
                st.markdown(full_response)
                st.session_state.messages.append({"role": "assistant", "content": full_response})
                
            except Exception as e:
                error_msg = f"Neural Engine Connection Error: {str(e)}"
                st.error(error_msg)
                st.session_state.messages.append({"role": "assistant", "content": error_msg})
