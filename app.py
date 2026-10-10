import streamlit as st
from groq import Groq
import os
import requests
import urllib.parse
from bs4 import BeautifulSoup
from PIL import Image
import streamlit.components.v1 as components

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
st.caption("2026 Enterprise Network: Smart 10s Autonomous Voice & Central Media Studio Active")

# सुरक्षित टोकन कॉन्फ़िगरेशन - अपनी असली API Key सिस्टम एनवायरनमेंट में सेट करें
GROQ_API_KEY = os.environ.get("GROQ_API_KEY", "") 
GROQ_MODEL = os.environ.get("GROQ_MODEL", "llama-3.3-70b")

if not GROQ_API_KEY:
    st.error("❌ GROQ_API_KEY नहीं मिली! कृपया इसे अपने Environment Variables में सेट करें।")
    st.stop()

client = Groq(api_key=GROQ_API_KEY)

# Session States Initializing
if "messages" not in st.session_state:
    st.session_state.messages = []

# पुराना चैट इतिहास स्क्रीन पर बनाए रखने के लिए लूप
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# 2. 📂 SIDEBAR: Control Panel Only
with st.sidebar:
    st.header("📂 ChatGPT Control Panel")
    st.info("Directly input prompts, create imagery, or request complex solutions.")
    st.markdown("---")
    
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
                const speechToText = event.results[0][0].transcript;
                statusText.innerHTML = '<b>Transmitting:</b> ' + speechToText;
                
                const parentDocs = window.parent.document;
                const streamlitInput = parentDocs.querySelector('textarea[data-testid="stChatInputTextArea"]');
                if (streamlitInput) {
                    streamlitInput.value = speechToText;
                    streamlitInput.dispatchEvent(new Event('input', { bubbles: true }));
                    setTimeout(() => {
                        const submitBtn = parentDocs.querySelector('button[data-testid="stChatInputSubmitButton"]');
                        if (submitBtn) { submitBtn.click(); }
                    }, 500);
                }
            };
            rec.onend = () => {
                voiceBtn.style.backgroundColor = '#1f8fff';
                voiceBtn.innerHTML = '🎙️ Tap to Speak';
            };
            rec.onerror = (e) => {
                clearTimeout(silenceTimer);
                statusText.innerText = 'Timeout or interrupted. Try again.';
            };
        } else {
            statusText.innerText = 'Microphone missing/unsupported.';
        }
    </script>
    """, height=140)

# 3. 🌐 लाइव वेब हब क्रॉलर फंक्शन (सुधरा हुआ)
def fetch_global_and_social_search(query_text):
    context = ""
    try:
        encoded_query = urllib.parse.quote(query_text)
        # DuckDuckGo का सही HTML सर्च यूआरएल पाथ
        search_url = f"https://duckduckgo.com{encoded_query}"
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'}
        
        search_response = requests.get(search_url, headers=headers, timeout=10)
        if search_response.status_code == 200:
            soup = BeautifulSoup(search_response.text, 'html.parser')
            links = soup.find_all('td', class_='result-snippet') or soup.find_all('a', class_='result__snippet')
            web_data = [l.text.strip() for l in links[:3]]
            if web_data:
                context = "\n".join([f"- Live Source: {d}" for d in web_data])
    except Exception:
        pass
    return context

# 4. 📸 CENTRAL MEDIA STUDIO
st.markdown("---")
st.markdown("### 📸 Upload Photo / Media / File (यहाँ से कुछ भी अपलोड करें):")
uploaded_file = st.file_uploader("Choose an image or document to analyze...", type=["jpg", "jpeg", "png"])

if uploaded_file:
    st.image(Image.open(uploaded_file), caption="Uploaded File Active", width=400)

# 5. 💬 MAIN CHAT BOX FLOW
user_input = st.chat_input("Search anything, Facebook/Instagram trends, generate photos...")

if user_input:
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.markdown(user_input)
        
    query_lower = user_input.lower()
    is_image_request = any(word in query_lower for word in ["photo", "image", "बनाओ", "banao", "generate", "picture"])
    
    if is_image_request:
        with st.chat_message("assistant"):
            with st.spinner("🎨 AG AI Image Studio: Generating HD Photo..."):
                try:
                    encoded_prompt = urllib.parse.quote(user_input)
                    # Pollinations AI का बिल्कुल सही एंडपॉइंट पाथ
                    image_url = f"https://pollinations.ai{encoded_prompt}?width=1024&height=1024&nologo=true"
                    
                    st.markdown(f"### 🎨 Generated Photo for: *\"{user_input}\"*")
                    st.image(image_url, use_container_width=True)
                    
                    st.session_state.messages.append({
                        "role": "assistant",
                        "content": f"📸 [Photo Generated Successfully] View Image here: {image_url}"
                    })
                except Exception as img_err:
                    st.error(f"Image Studio Error: {str(img_err)}")
    else:
        with st.chat_message("assistant"):
            with st.spinner("🔍 Deep searching live internet servers..."):
                web_context = fetch_global_and_social_search(user_input)
                media_info = " (Note: User has uploaded an image file on the dashboard for context.)" if uploaded_file else ""
                
                system_prompt = (
                    f"You are AG ChatGPT Plus, a world-class autonomous AI collaborator.{media_info} "
                    "Today's date is verified as Saturday, October 10, 2026. "
                    "Always combine the live global search data below with your neural networks to frame highly comprehensive responses."
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
                    st.markdown(full_response)
                    st.session_state.messages.append({"role": "assistant", "content": full_response})
                except Exception as e:
                    error_msg = f"Neural Engine Connection Error: {str(e)}"
                    st.error(error_msg)
                    st.session_state.messages.append({"role": "assistant", "content": error_msg})
