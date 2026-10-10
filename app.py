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
                const speechToText = event.results.transcript;
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
                
                # शॉर्ट उत्तर + लाइव डेटा प्राथमिकता नियम
                system_prompt = (
                    f"You are AG ChatGPT Plus, a world-class autonomous AI collaborator.{media_info} "
                    "Today's date is verified as Saturday, October 10, 2026. Current West Bengal CM is Suvendu Adhikari since May 2026.\n\n"
                    "CRITICAL RESPONSE RULE: Be extremely direct, concise, and to-the-point. Do NOT provide background history, geography, old context, or long descriptions. Answer ONLY exactly what the user asks for in the minimum possible words.\n\n"
                    "CONTEXT AWARENESS: Analyze the conversation history to understand pronouns or terms like 'lowest', 'next', 'why', or 'him' based on previous queries.\n\n"
                    "LIVE DATA DOMINANCE OVERRIDE: You MUST strictly believe the real-time internet data provided below. If it shows that a leader, CM, status, or event has changed recently in 2026, ignore your training cut-off completely and use the new live information immediately."
                )
                if web_context:
                    system_prompt += f"\n\n[UNIVERSAL LIVE WEB PIPELINE DATA (2026):]\n{web_context}"
                
                # ✅ फिक्स: सिस्टम प्रॉम्ट और पूरे पुराने चैट इतिहास को एक साथ कंबाइन करना
                api_messages = [{"role": "system", "content": system_prompt}]
                for msg in st.session_state.messages:
                    # केवल टेक्स्ट मैसेजेस को इतिहास में भेजें (इमेज जनरेशन लॉग्स को इग्नोर करें ताकि कॉन्टेक्स्ट साफ़ रहे)
                    if not msg["content"].startswith("📸 [Photo Generated"):
                        api_messages.append({"role": msg["role"], "content": msg["content"]})
                    
                try:
                    completion = client.chat.completions.create(
                        model=GROQ_MODEL,
                        messages=api_messages,
                        stream=False
                    )
                    full_response = completion.choices[0].message.content
                    st.markdown(full_response)
                    st.session_state.messages.append({"role": "assistant", "content": full_response})
                except Exception as e:
                    error_msg = f"Neural Engine Connection Error: {str(e)}"
                    st.error(error_msg)
                    st.session_state.messages.append({"role": "assistant", "content": error_msg})
