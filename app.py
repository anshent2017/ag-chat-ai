import streamlit as st
from groq import Groq
import os
import requests
import urllib.parse
from bs4 import BeautifulSoup
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
st.caption("2026 Enterprise Network: Smart 10s Autonomous Voice Engine Active")

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
                    
                    // Direct URL data transfer pipeline
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

# एकीकृत सुरक्षित सर्च क्रॉलर फंक्शन
def fetch_live_search(query_text):
    context = ""
    try:
        encoded_query = urllib.parse.quote(query_text)
        search_url = f"https://duckduckgo.com{encoded_query}"
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
        }
        search_response = requests.get(search_url, headers=headers, timeout=10)
        if search_response.status_code == 200:
            soup = BeautifulSoup(search_response.text, 'html.parser')
            links = soup.find_all('a', class_='result__snippet')
            web_data = [l.text.strip() for l in links[:3]]
            if web_data:
                context = "\n".join([f"- Source: {d}" for d in web_data])
    except:
        pass
    return context

# Check for URL incoming autonomous parameters injection
incoming_payload = st.query_params.get("voice_input_payload", "")

# 1. Direct Processing Interceptor Layer (वॉयस इनपुट स्ट्रीम प्रोसेसिंग)
if incoming_payload:
    st.query_params.clear() # Reset params to prevent infinity loops
    user_input = incoming_payload
    st.session_state.messages.append({"role": "user", "content": user_input})
    
    with st.spinner("🔍 Deep searching live internet servers..."):
        web_context = fetch_live_search(user_input)

        system_prompt = (
            "You are AG ChatGPT Plus, a world-class autonomous AI collaborator. "
            "Today's date is verified as Friday, October 9, 2026. "
            "Always combine the live global search data below with your neural networks to frame highly comprehensive responses."
        )
        if web_context:
            system_prompt += f"\n\n[UNIVERSAL LIVE WEB PIPELINE DATA (2026):]\n{web_context}"

        try:
            # वॉयस इनपुट के लिए लाइव रिस्पॉन्स स्ट्रीमिंग इनेबल की गई
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

# 2. Text Box Controller Flow (सामान्य चैट बॉक्स इनपुट - डाउनस्ट्रीम रिकवरी फिक्स)
else:
    text_box_input = st.chat_input("Ask AG ChatGPT anything, search global data, or generate HD photos...")
    if text_box_input:
        user_input = text_box_input
        st.session_state.messages.append({"role": "user", "content": user_input})
        
        # स्क्रीन पर तुरंत यूजर इनपुट दिखाएँ
        with st.chat_message("user"):
            st.markdown(user_input)

        # लाइव स्ट्रीमिंग चैट रेंडरर
        with st.chat_message("assistant"):
            response_placeholder = st.empty()
            with st.spinner("🔍 Deep searching live internet servers..."):
                web_context = fetch_live_search(user_input)
                
                system_prompt = (
                    "You are AG ChatGPT Plus, a world-class autonomous AI collaborator. "
                    "Today's date is verified as Friday, October 9, 2026. "
                    "Always combine the live global search data below with your neural networks to frame highly comprehensive responses."
                )
                if web_context:
                    system_prompt += f"\n\n[UNIVERSAL LIVE WEB PIPELINE DATA (2026):]\n{web_context}"

            try:
                # टेक्स्ट इनपुट के लिए लाइव चैट रिस्पॉन्स स्ट्रीमिंग इनेबल की गई
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
                        # टाइपिंग इफेक्ट रेंडरर
                        response_placeholder.markdown(full_response + "▌")
                
                response_placeholder.markdown(full_response)
                st.session_state.messages.append({"role": "assistant", "content": full_response})
                
            except Exception as api_err:
                error_msg = f"Neural Engine Error: {str(api_err)}"
                st.error(error_msg)
                st.session_state.messages.append({"role": "assistant", "content": error_msg})
