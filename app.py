import streamlit as st
from groq import Groq
import os
import requests
from streamlit_mic_recorder import speech_to_text

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
st.caption("2026 Enterprise Network: Official Native Voice Search & Global Web Crawler Active")

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
    
    # 🎙️ OFFICIAL NATIVE VOICE SEARCH (Bypasses all browser security blocks)
    st.markdown("### 🎙️ Bol Kar Search Karein:")
    voice_text = speech_to_text(
        start_prompt="🎙️ Start Speaking",
        stop_prompt="🛑 Stop & Process",
        language='hi', 
        use_container_width=True,
        key='native_voice'
    )
    
    if voice_text:
        st.success(f"Captured: {voice_text}")
        user_input = voice_text

# Text input configuration fallback (if not using voice)
if not user_input:
    text_box_input = st.chat_input("Ask AG ChatGPT anything, search global data, or generate HD photos...")
    if text_box_input:
        user_input = text_box_input

# Render Clean Chat History
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Main AI Processing Node Matrix
if user_input:
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
            # 🌐 RAW HYPER-TEXT WEB SEARCH
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

            # 🧠 CENTRAL INTELLECT CORE INSTRUCTIONS
            system_prompt = (
                "You are AG ChatGPT Plus, a world-class autonomous AI collaborator powered by absolute web access. "
                "Today's date is verified as Friday, October 9, 2026. "
                "You possess absolute capability across all fields: Medicine, Politics, Business, Advanced Software Architecture, Coding, History, and Creative Writing. "
                "Always combine the live global search data below with your neural networks to frame highly comprehensive, scannable responses using markdown format. "
                "If the user asks for a story ('kahani'), song ('gana'), or poetry ('shayari'), expand it with deep creative richness."
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
                
                # 🎯 FIXED SYNTAX HERE: Choices array ke index 0 alignment ko correct kiya hai crash se bachne ke liye
                full_response = completion.choices[0].message.content
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
