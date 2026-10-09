import streamlit as st
from groq import Groq
import os
import requests
import streamlit.components.v1 as components

#ChatGPT-Gemini Level Wide Production Configuration
st.set_page_config(page_title="AG ChatGPT Plus", page_icon="🧠", layout="wide")

st.markdown("""
    <style>
    .reportview-container { background: #1e1e2e; }
    h1 { color: #1f8fff; font-weight: 700; }
    .stChatMessage { border-radius: 10px; margin-bottom: 10px; }
    </style>
""", unsafe_allow_html=True)

st.title("🧠 AG ChatGPT Plus - Core Master Edition")
st.caption("2026 Active AI Framework: Voice, Live Scraping & HD Art Pipeline")

# Secure Token Configuration
GROQ_API_KEY = os.environ.get("GROQ_API_KEY", "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")
GROQ_MODEL = os.environ.get("GROQ_MODEL", "llama-3.3-70b")

client = Groq(api_key=GROQ_API_KEY)

if "messages" not in st.session_state:
    st.session_state.messages = []

# SIDEBAR: Standard Data Control Panel
with st.sidebar:
    st.header("📂 Data Panel")
    st.info("Directly input prompts, create imagery, or request complex solutions from the central agent.")

# Render Previous Session Logs
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# 🎙️ VOICE COMMAND PLUGIN (Speech Recognition Framework)
st.markdown("### 🎙️ Voice Assistant / Bol Kar Search Karein:")
components.html("""
    <div style="display: flex; align-items: center; gap: 10px; font-family: sans-serif;">
        <button id="start-btn" style="background-color: #1f8fff; color: white; border: none; padding: 10px 20px; border-radius: 20px; font-size: 16px; cursor: pointer; font-weight: bold;">
            🎙️ Start Speaking
        </button>
        <span id="output-text" style="color: #a0a0a0; font-style: italic; font-size: 14px;">Click and speak in Hindi or English...</span>
    </div>
    <script>
        const startBtn = document.getElementById('start-btn');
        const outputText = document.getElementById('output-text');
        const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
        if (SpeechRecognition) {
            const recognition = new SpeechRecognition();
            recognition.continuous = false;
            recognition.lang = 'hi-IN';
            recognition.interimResults = false;
            startBtn.addEventListener('click', () => {
                recognition.start();
                startBtn.style.backgroundColor = '#ff4b4b';
                startBtn.innerHTML = '🔴 Listening...';
            });
            recognition.onresult = (event) => {
                const transcript = event.results[0][0].transcript;
                outputText.innerHTML = '<b>You said:</b> ' + transcript;
                startBtn.style.backgroundColor = '#1f8fff';
                startBtn.innerHTML = '🎙️ Start Speaking';
                const inputArea = window.parent.document.querySelector('textarea[aria-label="Ask AG ChatGPT anything, search global data, or generate HD photos..."]');
                if(inputArea) {
                    inputArea.value = transcript;
                    inputArea.focus();
                }
            };
            recognition.onend = () => {
                startBtn.style.backgroundColor = '#1f8fff';
                startBtn.innerHTML = '🎙️ Start Speaking';
            };
        } else {
            outputText.innerText = 'Voice engine mismatch on this build.';
        }
    </script>
""", height=50)

# Main Terminal Input Box
if user_input := st.chat_input("Ask AG ChatGPT anything, search global data, or generate HD photos..."):
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.markdown(user_input)

    with st.chat_message("assistant"):
        response_placeholder = st.empty()
        
        # 🎨 AI IMAGE CONTEXT PROCESSING
        image_keywords = ["image", "photo", "picture", "draw", "banao", "banado", "create", "generate"]
        is_image_request = any(kw in user_input.lower() for kw in image_keywords)

        if is_image_request:
            with st.spinner("🎨 Generating high-quality visual data..."):
                try:
                    IMAGE_API_URL = "https://huggingface.co"
                    headers = {"Authorization": "Bearer hf_JdKxXvXvXvXvXvXvXvXvXvXvXvXvXvXv"}
                    
                    clean_prompt = user_input
                    for w in image_keywords + ["ki", "ko", "ek", "please", "of"]:
                        clean_prompt = clean_prompt.lower().replace(w, "").strip()
                    if not clean_prompt: clean_prompt = user_input

                    img_response = requests.post(IMAGE_API_URL, headers=headers, json={"inputs": clean_prompt}, timeout=45)
                    if img_response.status_code == 200:
                        st.image(img_response.content, caption=f"AI Artwork: {user_input}", use_container_width=True)
                        st.download_button(label="📥 Download HD Image", data=img_response.content, file_name="ag_art.png", mime="image/png")
                        full_response = "✨ Maine aapki imagination ke aadhar par image taiyar kar di hai."
                        response_placeholder.markdown(full_response)
                        st.session_state.messages.append({"role": "assistant", "content": full_response})
                    else:
                        st.error("Image generation service busy.")
                except Exception as img_err:
                    st.error(f"Image Error: {str(img_err)}")
        
        else:
            # 🌐 RAW HYPER-TEXT WEB SEARCH (Unlimited Scraping Framework)
            web_context = ""
            try:
                search_url = f"https://duckduckgo.com{user_input}+2026"
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

            # 🧠 CENTRAL INTELLECT CORE INSTRUCTIONS
            system_prompt = (
                "You are AG ChatGPT Plus, a world-class autonomous AI collaborator. "
                "Today's date is strictly verified as Friday, October 9, 2026. "
                "You possess absolute capability across all fields: Medicine, Politics, Business, Advanced Software Architecture, Coding, History, and Creative Writing. "
                "Always combine the live global search data below with your neural networks to frame highly comprehensive, scannable responses using markdown format. "
                "If the user submits a thought or partial text, expand it creatively into full scripts, stories, songs, or poetry as requested."
            )
            if web_context:
                system_prompt += f"\n\n[UNIVERSAL LIVE WEB PIPELINE DATA (2026):]\n{web_context}"

            # Static API Execution Layer (Fixed Indentation Framework)
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
                    if chunk.choices and chunk.choices[0].delta.content:
                        full_response += chunk.choices[0].delta.content
                        response_placeholder.markdown(full_response + "▌")
                
                response_placeholder.markdown(full_response)
                st.session_state.messages.append({"role": "assistant", "content": full_response})
            except Exception as api_err:
                st.error(f"Neural Engine Connection Error: {str(api_err)}")

    # 🎯 AUTOMATIC FOCUS WINDOW ALIGNMENT INTERACTION HACK
    components.html("""
        <script>
            window.parent.document.querySelector('section.main').scrollTo({
                top: window.parent.document.querySelector('section.main').scrollHeight,
                behavior: 'smooth'
            });
        </script>
    """, height=0)
