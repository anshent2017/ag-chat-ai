import streamlit as st
from groq import Groq
from duckduckgo_search import DDGS
import pypdf
import base64
import os

# Page Title & Layout Configuration
st.set_page_config(page_title="AG Chat.ai", page_icon="🤖")
st.title("🤖 AG Chat.ai - Ultimate Live")
st.caption("Cloud Powered: High-Speed AI Engine Running")

# Securely reading the key from Render settings
GROQ_API_KEY = os.environ.get("GROQ_API_KEY", "")

# Agar Environment Variable na mile toh backup ke liye direct key read karein
if not GROQ_API_KEY:
    GROQ_API_KEY = "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"

client = Groq(api_key=GROQ_API_KEY)

if "messages" not in st.session_state:
    st.session_state.messages = []

# SIDEBAR: Media Center for PDFs only
with st.sidebar:
    st.header("📂 Upload Center")
    uploaded_file = st.file_uploader("PDF Document upload karein", type=["pdf"])
    file_context = ""
    
    if uploaded_file is not None:
        st.success(f"Loaded: {uploaded_file.name}")
        with st.spinner("Scanning PDF lines..."):
            pdf_reader = pypdf.PdfReader(uploaded_file)
            pdf_text = ""
            for page in pdf_reader.pages[:5]:
                text = page.extract_text()
                if text: pdf_text += text
            file_context = f"\n[Context data from PDF file ({uploaded_file.name}):]\n{pdf_text[:2000]}"

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

        system_prompt = "You are AG Chat.ai, an elite cloud assistant. Answer accurately based on internet context or document context provided."
        if web_context:
            system_prompt += f"\n\nLive Internet Information:\n{web_context}"
        if file_context:
            system_prompt += f"\n\nDocument Data Context:\n{file_context}"

        # 🎯 Groq ka bilkul naya active model (Llama 3.3 70B Versatile)
        completion = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_input}
            ],
            stream=True,
        )

        full_response = ""
        for chunk in completion:
            if chunk.choices.delta.content:
                full_response += chunk.choices.delta.content
                response_placeholder.markdown(full_response + "▌")
        response_placeholder.markdown(full_response)

    st.session_state.messages.append({"role": "assistant", "content": full_response})
