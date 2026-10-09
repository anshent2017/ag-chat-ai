import streamlit as st
from groq import Groq
import os
import requests
import urllib.parse
import streamlit.components.v1 as components

# शक्तिशाली पैकेजों को सेफ़-मोड (Safe Import) में लोड करना ताकि सर्वर कभी क्रैश न हो
try:
    from bs4 import BeautifulSoup
except ImportError:
    BeautifulSoup = None

try:
    import wikipediaapi
except ImportError:
    wikipediaapi = None

try:
    import yfinance as yf
except ImportError:
    yf = None

try:
    from PIL import Image
except ImportError:
    Image = None

# ChatGPT-Gemini Level Wide Production Configuration
st.set_page_config(page_title="AG ChatGPT Plus", page_icon="🧠", layout="wide")

st.markdown("""
    <style>
    .reportview-container { background: #1e1e2e; }
    h1 { color: #1f8fff; font-weight: 700; }
    .stChatMessage { border-radius: 10px; margin-bottom: 10px; }
    </style>
""", unsafe_allow_html=True)

st.title("🧠 AG ChatGPT Plus - Absolute AI Engine")
st.caption("2026 Global Enterprise Network: Universal Search Crawler, Finance Matrix & Speech Sync Active")

# Secure Token Configuration
GROQ_API_KEY = os.environ.get("GROQ_API_KEY", "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")
GROQ_MODEL = os.environ.get("GROQ_MODEL", "llama-3.3-70b")

client = Groq(api_key=GROQ_API_KEY)

# Session States Initializing
if "messages" not in st.session_state:
    st.session_state.messages = []

# पुराना चैट इतिहास स्क्रीन पर हमेशा बनाए रखने के लिए लूप
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Unified Query Processing Controller Layer
user_input = ""

# 📂 SIDEBAR: ChatGPT Plus Control Panel & NATIVE VOICE SYSTEM
with st.sidebar:
    st.header("📂 ChatGPT Control Panel")
    st.info("Directly input prompts, create imagery, or request complex solutions.")
    st.markdown("---")
    
    # 🎙️ SMART 10-SECOND AUTONOMOUS VOICE SYSTEM (10s Buffer Active)
    st.markdown("### 🎙️ Bol Kar Search Karein:")
    components.html("""
        <div style="font-family: sans-serif; text-align: center; padding: 5px;">
            <button id="voice-start" style="background-color: #1f8fff; color: white; border: none; padding: 12px 24px; border-radius: 25px; font-size: 16px; cursor: pointer; font-weight: bold; width: 100%;">
                🎙️ Tap to Speak
            </button>
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
                
                rec.onsoundstart = () => {
                    clearTimeout(silenceTimer);
                };

                rec.onsoundend = () => {
                    statusText.innerText = 'Detecting silence... processing in 10s...';
                    silenceTimer = setTimeout(() => {
                        rec.stop();
                    }, 10000); 
                };

                rec.onresult = (event) => {
                    clearTimeout(silenceTimer);
                    const speechToText = event.results[0][0].transcript;
                    statusText.innerHTML = '<b>Transmitting:</b> ' + speechToText;
                    
                    const appUrl = new URL(window.parent.location.href);
                    appUrl.searchParams.set("voice_input_payload", speechToText);
                    window.parent.location.href = appUrl.href;
                };
                
                rec.onend = () => {
                    clearTimeout(silenceTimer);
                    voiceBtn.style.backgroundColor = '#1f8fff';
                    voiceBtn.innerHTML = '🎙️ Tap to Speak';
                };
                
                rec.onerror = (e) => {
                    clearTimeout(silenceTimer);
                    statusText.innerText = 'Timeout or Interrupted. Tap again.';
                };
            } else {
                statusText.innerText = 'Microphone connection missing.';
            }
        </script>
    """, height=100)

# 🌐 UNIVERSAL SEARCH & DATA CRAWLER ENGINE (A to Z Data Fetcher)
def universal_data_crawler(query_text):
    context = ""
    query_lower = query_text.lower()
    
    # 📈 टूल 1: रीयल-टाइम फाइनेंस/स्टॉक डेटा (यदि शेयर, स्टॉक, या प्राइस पूछा जाए)
    if yf and ("stock" in query_lower or "price" in query_lower or "share" in query_lower):
        try:
            # आसान ट्रैकिंग के लिए शब्दों को अलग करके टिकर खोजने का प्रयास
            words = query_text.upper().split()
            for word in words:
                if len(word) <= 5 and word.isalpha():
                    ticker = yf.Ticker(word)
                    info = ticker.history(period="1d")
                    if not info.empty:
                        close_price = info['Close'].iloc[-1]
                        context += f"\n- Live Finance Data ({word}): Last Closing Price is ${close_price:.2f}"
                        break
        except:
            pass

    # 📚 टूल 2: विकिपीडिया इन-डेप्थ रिसर्च (ऐतिहासिक या परिभाषा आधारित डेटा)
    if wikipediaapi and len(query_text.split()) < 4:
        try:
            wiki = wikipediaapi.Wikipedia('AG_Universal_Bot/1.0 (contact@example.com)', 'en')
            page = wiki.page(query_text)
            if page.exists():
                context += f"\n- Verified Context (Wikipedia): {page.summary[:600]}"
        except:
            pass

    # 🌐 टूल 3: डकडकगो लाइव ग्लोबल वेब पाइपलाइन (लाइव करंट अफेयर्स)
    try:
        encoded_query = urllib.parse.quote(query_text)
        search_url = f"https://duckduckgo.com{encoded_query}"
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
        }
        search_response = requests.get(search_url, headers=headers, timeout=10)
        
        if search_response.status_code == 200 and BeautifulSoup:
            soup = BeautifulSoup(search_response.text, 'html.parser')
            links = soup.find_all('a', class_='result__snippet')
            web_data = [l.text.strip() for l in links[:3]]
            if web_data:
                context += "\n" + "\n".join([f"- Live Global Source: {d}" for d in web_data])
    except:
        pass
        
    return context

# Check for URL incoming autonomous parameters injection
incoming_payload = st.query_params.get("voice_input_payload", "")

# 1. वॉयस इनपुट प्रोसेसिंग पाइपलाइन (Streaming Mode)
if incoming_payload:
    st.query_params.clear() 
    user_input = incoming_payload
    st.session_state.messages.append({"role": "user", "content": user_input})
    
    with st.spinner("🔍 Triggering Universal Deep Crawler Engine..."):
        web_context = universal_data_crawler(user_input)

        system_prompt = (
            "You are AG ChatGPT Plus, a world-class autonomous AI capable of handling absolute data, analytics, coding, and history. "
            "Today's date is verified as Friday, October 9, 2026. "
            "Always synthesize the multi-source live web pipeline data below with your knowledge base to give hyper-accurate responses."
        )
        if web_context:
            system_prompt += f"\n\n[UNIVERSAL LIVE WEB PIPELINE DATA (2026):]\n{web_context}"

        try:
            completion = client.chat.completions.create(
                model=GROQ_MODEL,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_input}
                ],
                stream=True
            )
            
            full_response = ""
            for chunk in completion:
                if chunk.choices[0].delta.content:
                    full_response += chunk.choices[0].delta.content
            
            st.session_state.messages.append({"role": "assistant", "content": full_response})
        except Exception as api_err:
            st.session_state.messages.append({"role": "assistant", "content": f"Neural Engine Error: {str(api_err)}"})
    st.rerun()

# 2. सामान्य चैट बॉक्स इनपुट प्रोसेसिंग पाइपलाइन (Streaming + Typing Effect)
else:
    text_box_input = st.chat_input("Ask AG ChatGPT anything (A-Z Search, Global Data, Finance Analytics)...")
    if text_box_input:
        user_input = text_box_input
        st.session_state.messages.append({"role": "user", "content": user_input})
        
        with st.chat_message("user"):
            st.markdown(user_input)

        with st.chat_message("assistant"):
            response_placeholder = st.empty()
            with st.spinner("🔍 Triggering Universal Deep Crawler Engine..."):
                web_context = universal_data_crawler(user_input)
                
                system_prompt = (
                    "You are AG ChatGPT Plus, a world-class autonomous AI capable of handling absolute data, analytics, coding, and history. "
                    "Today's date is verified as Friday, October 9, 2026. "
                    "Always synthesize the multi-source live web pipeline data below with your knowledge base to give hyper-accurate responses."
                )
                if web_context:
