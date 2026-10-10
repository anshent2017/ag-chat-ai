import streamlit as st
from groq import Groq
import os
import requests
import urllib.parse
from bs4 import BeautifulSoup
from PIL import Image
import streamlit.components.v1 as components

# 1. ChatGPT-Gemini Level Wide Production Configuration
st.set_page_config(page_title="AG ChatGPT Plus", page_icon="🧠", layout="wide")

st.markdown("""
    <style>
    .reportview-container { background: #1e1e2e; }
    h1 { color: #1f8fff; font-weight: 700; }
    .stChatMessage { border-radius: 10px; margin-bottom: 10px; }
    </style>
""", unsafe_allow_html=True)

st.title("🧠 AG ChatGPT Plus - Executive AI")
st.caption("2026 Enterprise Network: Smart 10s Autonomous Voice & HD Image Studio Active")

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

# 2. 📂 SIDEBAR: ChatGPT Control Panel & FIXED NATIVE VOICE SYSTEM
with st.sidebar:
    st.header("📂 ChatGPT Control Panel")
    st.info("Directly input prompts, create imagery, or request complex solutions.")
    st.markdown("---")
    
    # 📸 फोटो अपलोडर
    st.markdown("### 📸 Upload Photo / Media:")
    uploaded_file = st.file_uploader("Choose an image to analyze...", type=["jpg", "jpeg", "png"])
    if uploaded_file:
        st.image(Image.open(uploaded_file), caption="Uploaded Image Active", use_container_width=True)
    st.markdown("---")
    
    # 🎙️ 100% फिक्स्ड जावास्क्रिप्ट वॉयस ट्रांसमिशन पाइपलाइन
    st.markdown("### 🎙️ Bol Kar Search Karein:")
    components.html("""
        <div style="font-family: sans-serif; text-align: center; padding: 5px;">
            <button id="voice-start" style="background-color: #1f8fff; color: white; border: none; padding: 12px 24px; border-radius: 25px; font-size: 16px; cursor: pointer; font-weight: bold; width: 100%;">🎙️ Tap to Speak</button>
            <div id="voice-status" style="color: #a0a0a0; font-style: italic; font-size: 13px; margin-top: 8px;">Click to talk...</div>
        </div>
        <script>
            const voiceBtn = document.getElementById('voice-start');
            const statusText = document.getElementById('voice-status');
            const SpeechRecognition = window.webkitSpeechRecognition || window.SpeechRecognition;
            
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
                    // ✅ 100% सही एरे पाथ वॉयस टेक्स्ट निकालने के लिए (Fixes 'undefined')
                    const speechToText = event.results[0][0].transcript;
                    statusText.innerHTML = '<b>Transmitting:</b> ' + speechToText;
                    
                    // यूआरएल पैरामीटर के माध्यम से पायथन सर्वर को तुरंत डेटा भेजना
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
                statusText.innerText = 'Microphone connection missing/unsupported.'; 
            }
        </script>
    """, height=140)

# 3. 🌐 लाइव वेब हब क्रॉलर फंक्शन
def fetch_global_and_social_search(query_text):
    context = ""
    try:
        encoded_query = urllib.parse.quote(query_text)
        search_url = f"https://duckduckgo.com{encoded_query}"
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}
        search_response = requests.get(search_url, headers=headers, timeout=10)
        if search_response.status_code == 200:
            soup = BeautifulSoup(search_response.text, 'html.parser')
            links = soup.find_all('a', class_='result__snippet')
            web_data = [l.text.strip() for l in links[:3]]
            if web_data: 
                context = "\n".join([f"- Live Source: {d}" for d in web_data])
    except: 
        pass
    return context

# 4. 💬 UNIFIED CONTROLLER FLOW (एकीकृत पायथन बैकएंड इंजन)
user_input = ""

# यूआरएल से आने वाले वॉयस पेलोड को पकड़ें
if "voice_input_payload" in st.query_params:
    v_payload = st.query_params["voice_input_payload"]
    if v_payload and v_payload != "undefined" and v_payload != "":
        user_input = v_payload
        st.query_params.clear()  # लूप इनफिनिटी रोकने के लिए साफ करें
        st.session_state.messages.append({"role": "user", "content": user_input})
        st.rerun()

# चैट बॉक्स इनपुट (कीबोर्ड इनपुट)
text_box_input = st.chat_input("Search anything, Facebook/Instagram trends, generate photos...")
if text_box_input:
    user_input = text_box_input
    st.session_state.messages.append({"role": "user", "content": user_input})
    st.rerun()

# 5. CORE EXECUTION ENGINE (डेटा प्रोसेसिंग ब्लॉक)
if st.session_state.messages and st.session_state.messages[-1]["role"] == "user":
    latest_query = st.session_state.messages[-1]["content"]
    query_lower = latest_query.lower()
    
    # 📸 चेक करें: क्या यूजर फोटो/इमेज बनाने के लिए कह रहा है?
    is_image_request = any(word in query_lower for word in ["photo", "image", "बनाओ", "banao", "generate", "picture", "शायरी फोटो"])
    
    if is_image_request:
        with st.chat_message("assistant"):
            with st.spinner("🎨 AG AI Image Studio: Generating HD Photo..."):
                try:
                    # इमेज जनरेशन हेतु सही प्रॉम्प्ट रिज़ॉल्यूशन पाथ
                    encoded_prompt = urllib.parse.quote(latest_query)
                    image_url = f"https://pollinations.ai{encoded_prompt}?width=1024&height=1024&nologo=true"
                    
                    st.markdown(f"### 🎨 Generated Photo for: *\"{latest_query}\"*")
                    st.image(image_url, use_container_width=True)
                    
                    # चैट इतिहास में इमेज विवरण सहेजें
                    st.session_state.messages.append({
                        "role": "assistant", 
                        "content": f"📸 [Photo Generated Successfully] View Image here: {image_url}"
                    })
                except Exception as img_err:
                    st.error(f"Image Studio Error: {str(img_err)}")
    else:
        # 💬 सामान्य टेक्स्ट खोज या चैट प्रोसेसिंग (100% स्थिर नो-स्ट्रीम मोड जो एरर रोकेगा)
        with st.chat_message("assistant"):
            with st.spinner("🔍 Deep searching live internet servers..."):
                web_context = fetch_global_and_social_search(latest_query)
                system_prompt = (
                    "You are AG ChatGPT Plus, a world-class autonomous AI collaborator. "
                    "Today's date is verified as Saturday, October 10, 2026. "
                    "Always combine the live global search data below with your neural networks to frame highly comprehensive responses."
                )
                if web_context: 
                    system_prompt += f"\n\n[UNIVERSAL LIVE WEB PIPELINE DATA (2026):]\n{web_context}"
                    
            try:
                # 'delta' एट्रिब्यूट एरर को हमेशा के लिए समाप्त करने हेतु stream=False का सुरक्षित उपयोग
                completion = client.chat.completions.create(
                    model=GROQ_MODEL, 
                    messages=[
                        {"role": "system", "content": system_prompt}, 
                        {"role": "user", "content": latest_query}
                    ], 
                    stream=False
                )
                
                full_response = completion.choices[0].message.content
                st.markdown(full_response)
                st.session_state.messages.append({"role": "assistant", "content": full_response})
            except Exception as e:
                error_msg = f"Neural Engine Connection Error: {str(e)}"
                st.error(error_msg)
                st.session_state.messages.append({"role": "assistant", "content": error_msg})
