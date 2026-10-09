import streamlit as st
from groq import Groq
from duckduckgo_search import DDGS
import pypdf
import base64
import os

# Page Configurations
st.set_page_config(page_title="AG Chat.ai", page_icon="🤖", layout="centered")
st.title("🤖 AG Chat.ai - Ultimate Live")
st.caption("Cloud Powered: Photos, Live Search & PDF Scanning")
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
# 🎯 DIRECT API KEY INJECTION (Kanyat/Settings ka jhanjhat khatam)
# Niche quotes ke andar apni asli gsk_... waali API Key paste karein
GROQ_API_KEY = "gsk_YAHAN_APNI_REAL_KEY_PASTE_KAREIN"

if not GROQ_API_KEY or GROQ_API_KEY == "gsk_YAHAN_APNI_REAL_KEY_PASTE_KAREIN":
    st.error("Please add your actual Groq API Key inside the quotes in app.py code.")
    st.stop()

client = Groq(api_key=GROQ_API_KEY)

if "messages" not in st.session_state:
    st.session_state.messages = []

# SIDEBAR: Media Center for Photos and PDFs
with st.sidebar:
    st.header("📂 Upload Center")
    uploaded_file = st.file_uploader("Photo ya PDF upload karein", type=["png", "jpg", "jpeg", "pdf"])
    
    file_context = ""
    image_base64 = ""
    
    if uploaded_file is not None:
        st.success(f"Loaded: {uploaded_file.name}")
        
        # Condition 1: Agar Photo hai
        if uploaded_file.type in ["image/png", "image/jpeg"]:
            st.image(uploaded_file, use_container_width=True)
            bytes_data = uploaded_file.getvalue()
            image_base64 = base64.b64encode(bytes_data).decode('utf-8')
            file_context = "[User has uploaded an image. Visually scan the attached content.]"
            
        # Condition 2: Agar PDF Document hai
        elif uploaded_file.type == "application/pdf":
            with st.spinner("Scanning PDF lines..."):
                pdf_reader = pypdf.PdfReader(uploaded_file)
                pdf_text = ""
                for page in pdf_reader.pages[:5]:
                    text = page.extract_text()
                    if text: pdf_text += text
                file_context = f"\n[Context data from uploaded PDF file ({uploaded_file.name}):]\n{pdf_text[:2500]}"

# Display Chat History
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# User Chat Input
if user_input := st.chat_input("Ask AG Chat.ai anything..."):
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.markdown(user_input)

    with st.chat_message("assistant"):
        response_placeholder = st.empty()
        
        # Live Web Search Trigger
        web_context = ""
        try:
            with DDGS() as ddgs:
                search_results = [r for r in ddgs.text(user_input, max_results=2)]
                if search_results:
                    web_context = "\n".join([f"- {res['body']}" for res in search_results])
        except:
            pass

        # Smart Prompt Engineering for AI
        system_prompt = "You are AG Chat.ai, an elite cloud assistant. Answer accurately based on internet context or document context provided."
        if web_context:
            system_prompt += f"\n\nLive Internet Information:\n{web_context}"
        if file_context and not image_base64:
            system_prompt += f"\n\nDocument Data Context:\n{file_context}"

        content_structure = [{"type": "text", "text": f"{system_prompt}\n\nUser Prompt: {user_input}"}]
        
        if image_base64:
            content_structure.append({
                "type": "image_url",
                "image_url": {"url": f"data:image/jpeg;base64,{image_base64}"}
            })

        # Super-fast streaming response using stable vision model
        completion = client.chat.completions.create(
            model="llama-3.2-11b-vision-preview",
            messages=[{"role": "user", "content": content_structure}],
            stream=True,
        )

        full_response = ""
        for chunk in completion:
            if chunk.choices.delta.content:
                full_response += chunk.choices.delta.content
                response_placeholder.markdown(full_response + "▌")
        response_placeholder.markdown(full_response)

    st.session_state.messages.append({"role": "assistant", "content": full_response})
