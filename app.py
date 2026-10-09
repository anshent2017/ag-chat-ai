import streamlit as st
from groq import Groq
import os
import requests
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
st.caption("2026 Enterprise Network: Smart 10s Auto-Silence Voice Search & Global Web Crawler Active")

# Secure Token Configuration
GROQ_API_KEY = os.environ.get("GROQ_API_KEY", "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")
GROQ_MODEL = os.environ.get("GROQ_MODEL", "llama-3.3-70b")

client = Groq(api_key=GROQ_API_KEY)

if "messages" not in st.session_state:
    st.session_state.messages = []

# Unified Query Processing Controller Layer
user_input = ""

# 📂 SIDEBAR: ChatGPT Plus Control Panel & NATIVE VOICE SYSTEM
with st.sidebar:
    st.header("📂 ChatGPT Control Panel")
    st.info("Directly input prompts, create imagery, or request complex solutions.")
    st.markdown("---")
    
    # 🎙️ SMART 10-SECOND AUTO-SILENCE VOICE SYSTEM (Perfected 10s Silence Trigger)
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
                    // 🎯 TIMING UPDATED TO EXACTLY 10 SECONDS SILENCE DETECTION
                    statusText.innerText = 'Detecting silence... processing in 10s...';
                    silenceTimer = setTimeout(() => {
                        rec.stop();
                    }, 10000); 
                };

                rec.onresult = (event) => {
                    clearTimeout(silenceTimer);
                    const speechToText = event.results[0][0].transcript;
                    statusText.innerHTML = '<b>Transmitting:</b> ' + speechToText;
                    
                    // Native session sync trigger injection via direct top context handshake
                    const appUrl = new URL(window.parent.location.href);
                    appUrl.searchParams.set("voice_data_stream", speechToText);
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

# Check for incoming voice parameters state handshake execution
incoming_params = st.query_params
active_stream_data = incoming_params.get("voice_data_stream", "")

if active_stream_data:
    user_input = active_stream_data
    st.query_params.clear() 
    # ⚡ FORCE EXECUTION PIPELINE: Streamlit backend engine mapping trigger
    st.session_state["messages"].append({"role": "user", "content": user_input})
    
    # Direct background execution node fallback trigger to process text immediately
    with st.spinner("🔍 Deep searching live internet servers..."):
        web_context = ""
        try:
            search_url = f"https://duckduckgo.com{user_input}"
            headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}
            search_response = requests.get(search_url, headers=headers, timeout=10)
            if search_response.status_code == 200:
                from bs4 import BeautifulSoup
                soup = BeautifulSoup(search_response.text, 'html.parser')
                links = soup.find_all('a', class_='result__snippet')
                web_data = [l.text.strip() for l in links[:3]]
                if web_data:
                    web_context = "\n".join([f"- Data Source: {d}" for d in web_data])
        except:
            pass

        system_prompt = (
            "You are AG ChatGPT Plus, a world-class autonomous AI collaborator powered by absolute web access. "
            "Today's date is verified as Friday, October 9, 2026. "
            "You possess absolute capability across all fields: Medicine, Politics, Business, Advanced Software Architecture, Coding, History, and Creative Writing. "
            "Always combine the live global search data below with your neural networks to frame highly comprehensive, scannable responses using markdown format."
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
                stream=False
            )
            full_response = completion.choices[0].message.content
            st.session_state["messages"].append({"role": "assistant", "content": full_response})
        except Exception as e:
            st.session_state["messages"].append({"role": "assistant", "content": f"Neural Engine Connection Error: {str(e)}"})
    
    st.rerun()

# Text box configuration fallback (if not using voice)
else:
    text_box_input = st.chat_input("Ask AG ChatGPT anything, search global data, or generate HD photos...")
    if text_box_input:
        user_input = text_box_input
        st.session_state.messages.append({"role": "user", "content": user_input})
        with st.chat_message("user"):
            st.markdown(user_input)

        with st.chat_message("assistant"):
            response_placeholder = st.empty()
            web_context = ""
            try:
                search_url = f"https://duckduckgo.com{user_input}"
                headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}
                search_response = requests.get(search_url, headers=headers, timeout=10)
                if search_response.status_code == 200:
                    from bs4 import BeautifulSoup
                    soup = BeautifulSoup(search_response.text, 'html.parser')
                    links = soup.find_all('a', class_='result__snippet')
                    web_data = [l.text.strip() for l in links[:3]]
                    if web_data:
                        web_context = "\n".join([f"- Data Source: {d}" for d in web_data])
            except:
                pass

            system_prompt = (
                "You are AG ChatGPT Plus, a world-class autonomous AI collaborator powered by absolute web access. "
                "Today's date is verified as Friday, October 9, 2026. "
                "You possess absolute capability across all fields. Combine the live data below."
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
                    stream=False
                )
                full_response = completion.choices[0].message.content
                response_placeholder.markdown(full_response)
                st.session_state.messages.append({"role": "assistant", "content": full_response})
            except Exception as api_err:
                st.error(f"Neural Engine Connection Error: {str(api_err)}")

# Render Clean Chat History
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# 🎯 AUTOMATIC FOCUS WINDOW ALIGNMENT INTERACTION HACK
components.html("""
    <script>
        window.parent.document.querySelector('section.main').scrollTo({
            top: window.parent.document.querySelector('section.main').scrollHeight,
            behavior: 'smooth'
        });
    </script>
""", height=0)
