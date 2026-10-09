import streamlit as st
from groq import Groq
from duckduckgo_search import DDGS
import pypdf
import os

# Page Title & Layout Configuration
st.set_page_config(page_title="AG Chat.ai", page_icon="🤖")
st.title("🤖 AG Chat.ai - Fully Live 2026")
st.caption("Cloud Powered: Live Internet Data Integration Active")

# Securely reading the key from Render settings
GROQ_API_KEY = os.environ.get("GROQ_API_KEY", "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")
# Groq par abhi chalne wala stable endpoint
GROQ_MODEL = os.environ.get("GROQ_MODEL", "llama-3.3-70b")

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
        
        # 🌐 LIVE INTERNET CRAWLER (DuckDuckGo Live Search Engine)
        web_context = ""
        try:
            with DDGS() as ddgs:
                search_results = list(ddgs.text(user_input, max_results=2))
                if search_results:
                    web_context = "\n".join([f"- {res['body']}" for res in search_results])
        except Exception as e:
            pass

        # 🎯 STRICT COMMAND FOR 2026 LIVE UPDATES
        system_prompt = "You are AG Chat.ai, an elite live assistant. Current year is 2026. You MUST use the provided live search data to answer accurately."
        if web_context: 
            system_prompt += f"\n\n[CRITICAL: Live Internet Data from Today (2026):]\n{web_context}"
        if file_context: 
            system_prompt += f"\n\n[Document Data Context:]\n{file_context}"

        try:
            # ⚡ FIXED API STRUCTURE: Ab system prompt directly AI ke dimaag me jaayega
            completion = client.chat.completions.create(
                model=GROQ_MODEL,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_input}
                ],
                stream=False, 
            )

            # Display the real-time live data response
            full_response = completion.choices[0].message.content
            response_placeholder.markdown(full_response)
            st.session_state.messages.append({"role": "assistant", "content": full_response})
            
        except Exception as e:
            st.error(f"Groq API Response Error: {str(e)}")
