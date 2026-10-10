import streamlit as st
import os
import requests
import urllib.parse
import base64
from io import BytesIO
from bs4 import BeautifulSoup
from PIL import Image

# 1. Page Configuration (Wide Production Mode)
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
st.caption("2026 Enterprise Network: Stable HTTP Core Engine & Live Global Search Active")

# API URL Configuration - Official Completions Path
GROQ_API_KEY = os.environ.get("GROQ_API_KEY", "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")
GROQ_TEXT_MODEL = "llama-3.3-70b"
GROQ_VISION_MODEL = "llama-3.2-11b-vision-preview"
GROQ_API_URL = "https://groq.com"

# नया पृथक चैट स्पेस वेरिएबल (यह पुराने जमे हुए 405 कैश मेमोरी को 100% खत्म कर देगा)
if "ag_v7_stable_history" not in st.session_state:
    st.session_state["ag_v7_stable_history"] = []

# पूरी तरह से सुरक्षित चैट इतिहास रेंडरर
for message in st.session_state["ag_v7_stable_history"]:
    try:
        if isinstance(message, dict) and "role" in message and "content" in message:
            content_disp = str(message["content"])
            with st.chat_message(message["role"]):
                st.markdown(content_disp, unsafe_allow_html=True)
    except:
        pass

# 📂 SIDEBAR: Control Panel Only
with st.sidebar:
    st.header("📂 ChatGPT Control Panel")
    st.info("Directly input prompts, create imagery, or request live solutions.")
    st.markdown("---")
    
    if st.button("🔄 Reset Chat Session"):
        st.session_state["ag_v7_stable_history"] = []
        st.query_params.clear()
        st.rerun()
# 3. 🌐 लाइव वेब हब क्रॉलर फंक्शन (DuckDuckGo Live Scraper)
def fetch_global_and_social_search(query_text):
    context = ""
    if not query_text or len(query_text.strip()) < 2:
        return context
    try:
        encoded_query = urllib.parse.quote(query_text.strip())
        search_url = f"https://duckduckgo.com{encoded_query}"
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}
        search_response = requests.get(search_url, headers=headers, timeout=10)
        if search_response.status_code == 200:
            soup = BeautifulSoup(search_response.text, 'html.parser')
            links = soup.find_all('a', class_='result__snippet')
            web_data = [l.text.strip() for l in links[:3]]
            if web_data: context = "\n".join([f"- Live Source: {d}" for d in web_data])
    except: pass
    return context

# इमेज को बेस64 में बदलने का फंक्शन
def encode_image_to_base64(uploaded_file):
    buffered = BytesIO()
    image = Image.open(uploaded_file)
    image.thumbnail((800, 800))
    image.save(buffered, format="JPEG")
    return base64.b64encode(buffered.getvalue()).decode('utf-8')

# 4. 📸 CENTRAL MEDIA STUDIO (मुख्य स्क्रीन पर मीडिया अपलोडर)
st.markdown("---")
st.markdown("### 📸 Upload Photo / Media / File (यहाँ से इमेज अपलोड करें):")
uploaded_file = st.file_uploader("Choose an image to analyze...", type=["jpg", "jpeg", "png"])

if uploaded_file:
    st.image(Image.open(uploaded_file), caption="Uploaded File Active", width=300)

# 5. 💬 MAIN CHAT CONTROLLER FLOW (Keyboard Input Box)
user_input = st.chat_input("Search anything, Facebook/Instagram trends, generate photos...")

if user_input:
    st.session_state["ag_v7_stable_history"].append({"role": "user", "content": user_input})
    
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
                    st.session_state["ag_v7_stable_history"].append({
                        "role": "assistant", 
                        "content": f"📸 **Generated Photo for:** *\"{user_input}\"*\n\n<img src='{image_url}' width='100%' style='border-radius:10px;'/>"
                    })
                except Exception as img_err:
                    st.error(f"Image Studio Error: {str(img_err)}")
                        
    elif uploaded_file:
        with st.chat_message("assistant"):
            with st.spinner("🧠 AG Vision Engine: Analyzing uploaded media..."):
                try:
                    base64_image = encode_image_to_base64(uploaded_file)
                    headers = {
                        "Authorization": f"Bearer {GROQ_API_KEY}",
                        "Content-Type": "application/json"
                    }
                    payload = {
                        "model": GROQ_VISION_MODEL,
                        "messages": [
                            {
                                "role": "user",
                                "content": [
                                    {"type": "text", "text": f"The user asks: {user_input}. Look at the attached image carefully and answer comprehensively in Hindi or English."},
                                    {
                                        "type": "image_url",
                                        "image_url": {
                                            "url": f"data:image/jpeg;base64,{base64_image}"
                                        }
                                    }
                                ]
                            }
                        ],
                        "stream": False
                    }
                    
                    res = requests.post(GROQ_API_URL, json=payload, headers=headers, timeout=30)
                    
                    if res.status_code == 200:
                        full_response = res.json()['choices'][0]['message']['content']
                        st.markdown(full_response)
                        st.session_state["ag_v7_stable_history"].append({"role": "assistant", "content": full_response})
                    else:
                        st.error(f"Vision API Error Code {res.status_code}: {res.text}")
                except Exception as vision_err:
                    st.error(f"Vision Engine Connection Error: {str(vision_err)}")
                        
    else:
        with st.chat_message("assistant"):
            with st.spinner("🔍 Deep searching live internet servers..."):
                web_context = fetch_global_and_social_search(user_input)
                system_prompt = (
                    "You are AG ChatGPT Plus, a world-class autonomous AI collaborator. "
                    "Today's date is verified as Saturday, October 10, 2026. "
                    "Always combine the live global search data below with your neural networks to frame highly comprehensive and accurate responses based on 2026 timeline facts."
                )
                if web_context: 
                    system_prompt += f"\n\n[UNIVERSAL LIVE WEB PIPELINE DATA (2026):]\n{web_context}"
                    
            try:
                headers = {
                    "Authorization": f"Bearer {GROQ_API_KEY}",
                    "Content-Type": "application/json"
                }
                payload = {
                    "model": GROQ_TEXT_MODEL,
                    "messages": [
                        {"role": "system", "content": system_prompt},
                        {"role": "user", "content": user_input}
                    ],
                    "stream": False
                }
                
                res = requests.post(GROQ_API_URL, json=payload, headers=headers, timeout=30)
                
                if res.status_code == 200:
                    full_response = res.json()['choices'][0]['message']['content']
                    st.markdown(full_response)
                    st.session_state["ag_v7_stable_history"].append({"role": "assistant", "content": full_response})
                else:
                    st.error(f"Core API Error Code {res.status_code}: {res.text}")
                    
            except Exception as e:
                error_msg = f"Neural Engine Connection Error: {str(e)}"
                st.error(error_msg)
                st.session_state["ag_v7_stable_history"].append({"role": "assistant", "content": error_msg})
