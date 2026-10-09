import streamlit as st
from groq import Groq
from duckduckgo_search import DDGS
import pypdf
import base64
import os
import requests

# ChatGPT Style Premium UI Configuration
st.set_page_config(page_title="AG ChatGPT Pro", page_icon="🧠", layout="wide")

st.markdown("""
    <style>
    .reportview-container { background: #1e1e2e; }
    .stChatInput { position: fixed; bottom: 30px; width: 100%; }
    h1 { color: #1f8fff; font-weight: 700; }
    </style>
""", unsafe_allow_html=True)

st.title("🧠 AG ChatGPT Plus - Ultimate Edition")
st.caption("2026 Enterprise AI Server: Live Web Crawling, Advanced Coding & HD Image Generation Active")

# Secure Key Handshake
GROQ_API_KEY = os.environ.get("GROQ_API_KEY", "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")
GROQ_MODEL = os.environ.get("GROQ_MODEL", "llama-3.3-70b")

client = Groq(api_key=GROQ_API_KEY)

if "messages" not in st.session_state:
    st.session_state.messages = []

# 📂 SIDEBAR: ChatGPT Plus Advanced Control Center
with st.sidebar:
    st.header("📂 ChatGPT Control Panel")
    st.info("Upload any Company Data, PDF, Text, or Code File below for deep scanning.")
    uploaded_file = st.file_uploader("Document / Code Scanner", type=["pdf", "txt", "py", "html", "css", "js"])
    
    file_context = ""
    if uploaded_file is not None:
        st.success(f"✓ Scanned: {uploaded_file.name}")
        if uploaded_file.name.endswith(".pdf"):
            pdf_reader = pypdf.PdfReader(uploaded_file)
            pdf_text = "".join([page.extract_text() for page in pdf_reader.pages[:10] if page.extract_text()])
            file_context = f"\n[Uploaded PDF Document Content:]\n{pdf_text[:4000]}"
        else:
            file_context = f"\n[Uploaded File Content:]\n{uploaded_file.getvalue().decode('utf-8')[:4000]}"

    st.markdown("---")
    st.markdown("### Quick Commands Shortcut:")
    st.write("- `generate image of a cyberpunk city`")
    st.write("- `search latest financial data of Apple Inc.`")
    st.write("- `write a python program for snake game`")

# Display Premium Chat Layout
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Main Chat Input (Universal Command Box)
if user_input := st.chat_input("Ask AG ChatGPT anything, search live data, or generate HD photos..."):
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.markdown(user_input)

    with st.chat_message("assistant"):
        response_placeholder = st.empty()
        
        # 🎨 SUPER FLEXIBLE SMART IMAGE DETECTION (Hindi + English All Keywords Added)
        image_keywords = ["image", "photo", "picture", "draw", "paint", "banao", "banado", "banaiye", "create", "generate", "illustration"]
        is_image_request = any(keyword in user_input.lower() for keyword in image_keywords)

        if is_image_request:
            with st.spinner("🎨 AG ChatGPT is drawing your imagination in Ultra HD..."):
                try:
                    # Industry standard open-source ultra-realistic diffusion model
                    IMAGE_API_URL = "https://huggingface.co"
                    headers = {"Authorization": "Bearer hf_JdKxXvXvXvXvXvXvXvXvXvXvXvXvXvXv"}
                    
                    # English Translation prompt optimization injection
                    clean_prompt = user_input
                    # Clean words to make pure prompt for FLUX engine
                    for word in image_keywords + ["ki", "ko", "ek", "please"]:
                        clean_prompt = clean_prompt.lower().replace(word, "").strip()
                    
                    # If empty prompt after cleaning, restore full user input
                    if not clean_prompt:
                        clean_prompt = user_input

                    img_response = requests.post(IMAGE_API_URL, headers=headers, json={"inputs": clean_prompt}, timeout=50)
                    
                    if img_response.status_code == 200:
                        st.image(img_response.content, caption=f"AI Artwork: {user_input}", use_container_width=True)
                        
                        st.download_button(
                            label="📥 Download HD Image",
                            data=img_response.content,
                            file_name=f"ag_ai_{clean_prompt.replace(' ', '_')}.png",
                            mime="image/png"
                        )
                        
                        full_response = f"✨ Maine aapki command ke aadhar par High-Quality photo upar generate kar di hai. Aap use download button se save kar sakte hain!"
                        response_placeholder.markdown(full_response)
                        st.session_state.messages.append({"role": "assistant", "content": full_response})
                    else:
                        st.error("Image Server temporary busy. Please wait 10 seconds and tap send icon again.")
                except Exception as e:
                    st.error(f"Image Module Error: {str(e)}")
        
        else:
            # 🌐 LIVE DEEP WEB SEARCH CRAWLER ENGINE
            web_context = ""
            with st.spinner("🔍 Deep searching live internet servers for real-time 2026 data..."):
                try:
                    with DDGS() as ddgs:
                        search_results = list(ddgs.text(f"{user_input} latest facts 2026", max_results=3))
                        if search_results:
                            web_context = "\n".join([f"Source [{res['title']}]: {res['body']}" for res in search_results])
                except:
                    pass

            # 🧠 CHATGPT MASTER PROMPT SYSTEM
            system_prompt = (
                "You are AG ChatGPT Plus, an advanced enterprise level AI assistant. "
                "Today is Friday, October 9, 2026. You possess elite capabilities in complex software engineering, coding, financial analysis, data lookup, and content writing. "
                "You MUST deeply analyze the real-time internet web data provided below and combine it with your knowledge to give complete, comprehensive, textbook-level structural answers. "
                "Provide detailed code blocks using markdown formatting if requested."
            )
            
            if web_context: 
                system_prompt += f"\n\n[CRITICAL: Live Real-Time Internet Data Pipe (2026):]\n{web_context}"
            if file_context: 
                system_prompt += f"\n\n[Uploaded Secure File Context Data:]\n{file_context}"

            try:
                completion = client.chat.completions.create(
                    model=GROQ_MODEL,
                    messages=[
                        {"role": "system", "content": system_prompt},
                        {"role": "user", "content": user_input}
                    ],
                    stream=False,
                )

                full_response = completion.choices[0].message.content
                response_placeholder.markdown(full_response)
                st.session_state.messages.append({"role": "assistant", "content": full_response})
                
            except Exception as e:
                st.error(f"Neural Engine Connection Error: {str(e)}")
