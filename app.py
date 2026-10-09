import streamlit as st
from groq import Groq
from duckduckgo_search import DDGS
import pypdf
import base64
import os

st.set_page_config(page_title="AG Chat.ai", page_icon="🤖")
st.title("🤖 AG Chat.ai - Live")

GROQ_API_KEY = os.environ.get("GROQ_API_KEY", "")

if not GROQ_API_KEY:
    st.error("Please add GROQ_API_KEY in Render Settings.")
    st.stop()

client = Groq(api_key=GROQ_API_KEY)

if "messages" not in st.session_state:
    st.session_state.messages = []

with st.sidebar:
    st.header("📂 Upload Center")
    uploaded_file = st.file_uploader("Photo ya PDF", type=["png", "jpg", "jpeg", "pdf"])
    file_context = ""
    image_base64 = ""
    
    if uploaded_file is not None:
        if uploaded_file.type in ["image/png", "image/jpeg"]:
            st.image(uploaded_file, use_container_width=True)
            image_base64 = base64.b64encode(uploaded_file.getvalue()).decode('utf-8')
        elif uploaded_file.type == "application/pdf":
            pdf_reader = pypdf.PdfReader(uploaded_file)
            pdf_text = "".join([page.extract_text() for page in pdf_reader.pages[:3] if page.extract_text()])
            file_context = f"\n[PDF Content:]\n{pdf_text[:1500]}"

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if user_input := st.chat_input("Ask anything..."):
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.markdown(user_input)

    with st.chat_message("assistant"):
        response_placeholder = st.empty()
        
        web_context = ""
        try:
            with DDGS() as ddgs:
                search_results = [r for r in ddgs.text(user_input, max_results=2)]
                if search_results:
                    web_context = "\n".join([f"- {res['body']}" for res in search_results])
        except:
            pass

        system_prompt = "You are AG Chat.ai. Answer accurately."
        if web_context: system_prompt += f"\n\nLive Search:\n{web_context}"
        if file_context: system_prompt += f"\n\nFile:\n{file_context}"

        content_structure = [{"type": "text", "text": f"{system_prompt}\n\nUser: {user_input}"}]
        
        if image_base64:
            content_structure.append({
                "type": "image_url",
                "image_url": {"url": f"data:image/jpeg;base64,{image_base64}"}
            })

        # 🎯 Yeh universal model hamesha active rehta hai aur text-photo dono handles karta hai
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
