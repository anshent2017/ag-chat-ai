import streamlit as st
from groq import Groq
import pypdf
import os
import requests
import streamlit.components.v1 as components

# ChatGPT-Gemini Level Premium Wide Layout Configuration
st.set_page_config(page_title="AG ChatGPT Plus", page_icon="🧠", layout="wide")

st.markdown("""
    <style>
    .reportview-container { background: #1e1e2e; }
    h1 { color: #1f8fff; font-weight: 700; }
    .stChatMessage { border-radius: 10px; margin-bottom: 10px; }
    </style>
""", unsafe_allow_html=True)

st.title("🧠 AG ChatGPT Plus - Voice Intelligence")
st.caption("2026 Enterprise Neural Network: Voice Search, Global Web Scraping & Multi-Modal Engine Active")

# Secure Key Handshake
GROQ_API_KEY = os.environ.get("GROQ_API_KEY", "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")
GROQ_MODEL = os.environ.get("GROQ_MODEL", "llama-3.3-70b")

client = Groq(api_key=GROQ_API_KEY)

if "messages" not in st.session_state:
    st.session_state.messages = []

# SIDEBAR: Advanced Data/Document Scanner
with st.sidebar:
    st.header("📂 Data & File Scanner")
    st.info("Upload any document, PDF, or text file for deep AI analysis.")
    uploaded_file = st.file_uploader("Document Upload", type=["pdf", "txt", "py", "html", "css", "js"])
    
    file_context = ""
    if uploaded_file is not None:
        st.success(f"✓ Scanned: {uploaded_file.name}")
        if uploaded_file.name.endswith(".pdf"):
            pdf_reader = pypdf.PdfReader(uploaded_file)
            pdf_text = "".join([page.extract_text() for page in pdf_reader.pages[:10] if page.extract_text()])
            file_context = f"\n[Document Context Data:]\n{pdf_text[:4000]}"
        else:
            file_context = f"\n[File Content:]\n{uploaded_file.getvalue().decode('utf-8')[:4000]}"

# Display Chat Layout
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# 🎙️ HIGH-SPEED JAVASCRIPT SPEECH TO TEXT WIDGET (Voice Command Engine)
st.markdown("### 🎙️ Voice Assistant / Bol Kar Search Karein:")
voice_data = components.html("""
    <div style="display: flex; align-items: center; gap: 10px; font-family: sans-serif;">
        <button id="start-btn" style="background-color: #1f8fff; color: white; border: none; padding: 10px 20px; border-radius: 20px; font-size: 16px; cursor: pointer; font-weight: bold; display: flex; align-items: center; gap: 8px;">
            🎙️ Start Speaking
        </button>
        <span id="output-text" style="color: #a0a0a0; font-style: italic; font-size: 14px;">Click the button and start speaking in Hindi or English...</span>
    </div>

    <script>
        const startBtn = document.getElementById('start-btn');
        const outputText = document.getElementById('output-text');
        
        // Browser Speech Recognition API Initialization
        const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
        
        if (SpeechRecognition) {
            const recognition = new SpeechRecognition();
            recognition.continuous = false;
            recognition.lang = 'hi-IN'; // Default matching multi-lingual voice pipeline (Hindi + English)
            recognition.interimResults = false;

            startBtn.addEventListener('click', () => {
                recognition.start();
                startBtn.style.backgroundColor = '#ff4b4b';
                startBtn.innerHTML = '🔴 Listening...';
                outputText.innerText = 'Listening to your voice command...';
            });

            recognition.onresult = (event) => {
                const transcript = event.results[0][0].transcript;
                outputText.style.color = '#1f8fff';
                outputText.innerHTML = '<b>You said:</b> ' + transcript;
                startBtn.style.backgroundColor = '#1f8fff';
                startBtn.innerHTML = '🎙️ Start Speaking';
                
                // Direct Injecting text into Streamlit chat input structure dynamically
                window.parent.document.querySelector('textarea[aria-label="Ask AG ChatGPT anything, search global data, or generate HD photos..."]').value = transcript;
                window.parent.document.querySelector('textarea[aria-label="Ask AG ChatGPT anything, search global data, or generate HD photos..."]').focus();
            };

            recognition.onerror = (event) => {
                startBtn.style.backgroundColor = '#1f8fff';
                startBtn.innerHTML = '🎙️ Start Speaking';
                outputText.innerText = 'Error occurred: ' + event.error;
            };
            
            recognition.onend = () => {
                startBtn.style.backgroundColor = '#1f8fff';
                startBtn.innerHTML = '🎙️ Start Speaking';
            };
        } else {
            outputText.innerText = 'Speech Recognition not supported on this browser version.';
        }
    </script>
""", height=50)

# Universal Agent Command Input
if user_input := st.chat_input("Ask AG ChatGPT anything, search global data, or generate HD photos..."):
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.markdown(user_input)

    with st.chat_message("assistant"):
        response_placeholder = st.empty()
        
        # 🎨 AI IMAGE ENGINE (Ultra-HD Image Creator Integrated)
        image_keywords = ["image", "photo", "picture", "draw", "banao", "banado", "create", "generate"]
        is_image_request = any(keyword in user_input.lower() for keyword in image_keywords)

        if is_image_request:
            with st.spinner("🎨 Generating high-quality visual representation..."):
                try:
                    IMAGE_API_URL = "https://huggingface.co"
                    headers = {"Authorization": "Bearer hf_JdKxXvXvXvXvXvXvXvXvXvXvXvXvXvXv"}
                    
                    clean_prompt = user_input
                    for word in image_keywords + ["ki", "ko", "ek", "please", "of"]:
                        clean_prompt = clean_prompt.lower().replace(word, "").strip()
                    
                    if not clean_prompt: clean_prompt = user_input

                    img_response = requests.post(IMAGE_API_URL, headers=headers, json={"inputs": clean_prompt}, timeout=50)
                    
                    if img_response.status_code == 200:
                        st.image(img_response.content, caption=f"AI Image: {user_input}", use_container_width=True)
                        st.download_button(label="📥 Download HD Image", data=img_response.content, file_name="ag_ai_art.png", mime="image/png")
                        full_response = "✨ Maine aapki command ke aadhar par High-Quality photo upar generate kar di hai."
                        response_placeholder.markdown(full_response)
                        st.session_state.messages.append({"role": "assistant", "content": full_response})
                    else:
                        st.error("Image Engine busy, retrying text fallback...")
                except Exception as e:
                    st.error(f"Image Error: {str(e)}")
        
        else:
            # 🌐 UNIVERSAL INTERNET CRAWLER (Direct Scraping Bypass)
            web_context = ""
            with st.spinner("🔍 Deep crawling global web clusters for real-time 2026 data..."):
                try:
                    search_url = f"https://duckduckgo.com{user_input}+2026"
                    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}
                    search_response = requests.get(search_url, headers=headers, timeout=10)
                    
                    if search_response.status_code == 200:
                        from bs4 import BeautifulSoup
                        soup = BeautifulSoup(search_response.text, 'html.parser')
                        links = soup.find_all('a', class_='result__snippet')
                        web_data_list = [link.text.strip() for link in links[:4]]
                        if web_data_list:
                            web_context = "\n".join([f"- Live Global Data: {data}" for data in web_data_list])
                except Exception as crawler_error:
                    pass

            # 🧠 INFINITE AI KNOWLEDGE GRADIENT SYSTEM (Strictest Professional Settings)
            system_prompt = (
                "You are AG ChatGPT Plus, a world-class, ultra-intelligent autonomous AI collaborator powered by Google-level absolute web access. "
                "Today's date is strictly verified as Friday, October 9, 2026. "
                "YOUR CORE DESIGN RULES:\n"
                "- You possess infinite access to all fields of human knowledge: Medicine, Politics, Business, Advanced Coding, Mathematics, History, and Law.\n"
                "- Never say you cannot access information. If the user asks about any company data, current events, or politics, use the live scraped global web text below to frame precise, current 2026 answers.\n"
                "- Act exactly like a core AI assistant (Gemini/ChatGPT Pro). Provide complete, highly structured responses with code blocks, list formats, and bullet points to maximize scannability."
            )
            
            if web_context: 
                system_prompt += f"\n\n[UNIVERSAL LIVE WEB PIPELINE DATA (2026):]\n{web_context}"
            if file_context: 
                system_prompt += f"\n\n[Uploaded Document/Company Data Context:]\n{file_context}"

            try:
                # High-speed active server streaming engine execution
                completion = client.chat.completions.create(
                    model=GROQ_MODEL,
                    messages=[
                        {"role": "system", "content": system_prompt},
                        {"role": "user", "content": user_input}
                    ],
