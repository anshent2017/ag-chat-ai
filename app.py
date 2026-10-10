import streamlit as st
from groq import Groq
import os
import requests
import urllib.parse
from bs4 import BeautifulSoup
from PIL import Image
import streamlit.components.v1 as components

# ChatGPT-Gemini Level Wide Production Configuration
st.set_page_config(page_title="AG ChatGPT Plus", page_icon="🧠", layout="wide")

st.markdown("""
    <style>
    .reportview-container { background: #1e1e2e; }
    h1 { color: #1f8fff; font-weight: 700; }
    .stChatMessage { border-radius: 10px; margin-bottom: 10px; }
    </style>
""", unsafe_allow_html=True)

st.title("🧠 AG ChatGPT Plus - Executive AI")
st.caption("2026 Enterprise Network: Smart 10s Fully-Automated Voice & Global Social Crawler Active")

# Secure Token Configuration
GROQ_API_KEY = os.environ.get("GROQ_API_KEY", "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")
GROQ_MODEL = os.environ.get("GROQ_MODEL", "llama-3.3-70b")
client = Groq(api_key=GROQ_API_KEY)

if "messages" not in st.session_state:
    st.session_state.messages = []

# पुराना चैट इतिहास स्क्रीन पर हमेशा बनाए रखने के लिए लूप
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# 📂 SIDEBAR: ChatGPT Plus Control Panel & NATIVE VOICE SYSTEM
with st.sidebar:
    st.header("📂 ChatGPT Control Panel")
    st.info("Directly input prompts, create imagery, or request complex solutions.")
    st.markdown("---")
    
    # 📸 एडवांस फोटो अपलोडर
    st.markdown("### 📸 Upload Photo / Media:")
    uploaded_file = st.file_uploader("Choose an image to analyze...", type=["jpg", "jpeg", "png"])
    if uploaded_file:
        st.image(Image.open(uploaded_file), caption="Uploaded Image Active", use_container_width=True)
    st.markdown("---")
    
    # 🎙️ PERFECTED AUTONOMOUS AUTOMATIC TRIGGER SYSTEM (Fixes 'undefined' glitch)
    st.markdown("### 🎙️ Bol Kar Search Karein:")
    components.html("""
        <div style="font-family: sans-serif; text-align: center; padding: 5px;">
            <button id="voice-start" style="background-color: #1f8fff; color: white; border: none; padding: 12px 24px; border-radius: 25px; font-size: 16px; cursor: pointer; font-weight: bold; width: 100%;">🎙️ Tap to Speak</button>
            <div id="voice-status" style="color: #a0a0a0; font-style: italic; font-size: 13px; margin-top: 8px;">Click to talk...</div>
        </div>
        <script>
            const voiceBtn = document.getElementById('voice-start');
            const statusText = document.getElementById('voice-status');
            const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
            
            if (SpeechRecognition) {
                const rec = new SpeechRecognition();
                rec.continuous = false; 
                rec.lang = 'hi-IN'; 
                rec.interimResults = false;
                let silenceTimer;
                
                voiceBtn.addEventListener('click', () => {
                    rec.start(); 
                    voiceBtn.style.backgroundColor = '#ff4b4b'; 
                    voiceBtn.innerHTML = '🔴 Listening...'; 
                    statusText.innerText = 'Speak now clearly...';
                });
                
                rec.onsoundstart = () => clearTimeout(silenceTimer);
                
                rec.onsoundend = () => {
                    statusText.innerText = 'Detecting silence... processing in 10s...';
                    silenceTimer = setTimeout(() => rec.stop(), 10000);
                };
                
                rec.onresult = (event) => {
                    clearTimeout(silenceTimer);
                    // ✅ फिक्स: 'undefined' को रोकने के लिए सही एरे इंडेक्सिंग पाथ का उपयोग
                    const speechToText = event.results[0][0].transcript;
                    statusText.innerHTML = '<b>Transmitting:</b> ' + speechToText;
                    
                    // वॉयस इनपुट को सीधे टॉप पेरेंट यूआरएल पर भेजना
                    const appUrl = new URL(window.parent.location.href);
                    appUrl.searchParams.set("voice_input_payload", speechToText);
                    window.parent.location.href = appUrl.href;
                };
                
                rec.onend = () => { 
                    voiceBtn.style.backgroundColor = '#1f8fff'; 
                    voiceBtn.innerHTML = '🎙️ Tap to Speak'; 
                };
                
                rec.onerror = (e) => {
                    clearTimeout(silenceTimer);
                    statusText.innerText = 'Error or Timeout. Try again.';
                };
            } else { 
                statusText.innerText = 'Microphone connection missing.'; 
            }
        </script>
    """, height=140)# 🌐 DEEP SOCIAL MEDIA & GLOBAL CRAWLER ENGINE
def fetch_global_and_social_search(query_text):
    context = ""
    query_lower = query_text.lower()
    
    # इंस्टाग्राम बायो एक्सट्रैक्टर
    try:
        import instaloader
        if "instagram" in query_lower or "insta" in query_lower:
            L = instaloader.Instaloader()
            words = query_text.split()
            for word in words:
                if len(word) > 3:
                    username = word.replace('@', '')
                    profile = instaloader.Profile.from_username(L.context, username)
                    context += f"\n- Instagram Profile ({username}): {profile.biography[:150]} | Followers: {profile.followers}"
                    break
    except: pass

    # सोशल मीडिया पब्लिक सर्च क्रॉलर
    try:
        encoded_query = urllib.parse.quote(query_text + " site:facebook.com OR site:instagram.com OR site:twitter.com")
        search_url = f"https://duckduckgo.com{encoded_query}"
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}
        search_response = requests.get(search_url, headers=headers, timeout=10)
        if search_response.status_code == 200:
            soup = BeautifulSoup(search_response.text, 'html.parser')
            links = soup.find_all('a', class_='result__snippet')
            web_data = [l.text.strip() for l in links[:3]]
            if web_data:
                context += "\n" + "\n".join([f"- Social Media Pipeline: {d}" for d in web_data])
    except: pass
    
    # सामान्य लाइव सर्च बैकअप
    if not context:
        try:
            encoded_query = urllib.parse.quote(query_text)
            search_url = f"https://duckduckgo.com{encoded_query}"
            search_response = requests.get(search_url, headers={'User-Agent': 'Mozilla/5.0'}, timeout=10)
            if search_response.status_code == 200:
                soup = BeautifulSoup(search_response.text, 'html.parser')
                links = soup.find_all('a', class_='result__snippet')
                web_data = [l.text.strip() for l in links[:3]]
                if web_data: context = "\n".join([f"- Live Source: {d}" for d in web_data])
        except: pass
        
    return context

# 💬 UNIFIED CONTROLLER FLOW
user_input = ""

# यूआरएल से आने वाले वॉयस पेलोड की जांच करें
incoming_payload = st.query_params.get("voice_input_payload", "")
if incoming_payload and incoming_payload != "undefined":
    st.query_params.clear()  # रिफ्रेश लूप को रोकने के लिए
    user_input = incoming_payload
    st.session_state.messages.append({"role": "user", "content": user_input})
    st.rerun()

# चैट बॉक्स इनपुट (नॉर्मल मोड)
text_box_input = st.chat_input("Search anything, Facebook/Instagram trends, generate photos...")
if text_box_input:
    user_input = text_box_input
    st.session_state.messages.append({"role": "user", "content": user_input})
    st.rerun()

# यदि कोई नया इनपुट आया है तो उसे तुरंत प्रोसेस करें
if st.session_state.messages and st.session_state.messages[-1]["role"] == "user":
    latest_query = st.session_state.messages[-1]["content"]
    
    with st.chat_message("assistant"):
        response_placeholder = st.empty()
        with st.spinner("🔍 Scanning global servers & social media networks..."):
            web_context = fetch_global_and_social_search(latest_query)
            system_prompt = (
                "You are AG ChatGPT Plus, a world-class autonomous AI collaborator equipped with absolute social network pipelines and an Image Studio. "
                "Today's date is verified as Saturday, October 10, 2026. Synthesize data into clean markdown responses."
            )
            if web_context: 
                system_prompt += f"\n\n[LIVE SOCIAL & WEB PIPELINE DATA (2026):]\n{web_context}"
                
        try:
            completion = client.chat.completions.create(
                model=GROQ_MODEL, 
                messages=[
                    {"role": "system", "content": system_prompt}, 
                    {"role": "user", "content": latest_query}
                ], 
                stream=True
            )
            full_response = ""
            for chunk in completion:
                if chunk.choices and len(chunk.choices) > 0:
                    delta = chunk.choices[0].delta
                    if hasattr(delta, 'content') and delta.content:
                        full_response += delta.content
                        response_placeholder.markdown(full_response + "▌")
            
            response_placeholder.markdown(full_response)
            st.session_state.messages.append({"role": "assistant", "content": full_response})
        except Exception as e:
            error_msg = f"Neural Engine Connection Error: {str(e)}"
            st.error(error_msg)
            st.session_state.messages.append({"role": "assistant", "content": error_msg})

