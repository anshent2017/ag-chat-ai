import streamlit as st
from groq import Groq
from duckduckgo_search import DDGS
import pypdf
import os
import requests
import streamlit.components.v1 as components

# ChatGPT Style Premium UI Configuration
st.set_page_config(page_title="AG ChatGPT Pro", page_icon="🧠", layout="wide")

st.markdown("""
    <style>
    .reportview-container { background: #1e1e2e; }
    h1 { color: #1f8fff; font-weight: 700; }
    .stChatMessage { border-radius: 10px; margin-bottom: 10px; }
    </style>
""", unsafe_allow_html=True)

st.title("🧠 AG ChatGPT Plus - Ultimate 2026 Edition")
st.caption("2026 Mega Server: Live Crawler, HD Images, Creative Writer & Auto-Scroll Active")

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
            file_context = f"\n[Uploaded PDF Content:]\n{pdf_text[:4000]}"
        else:
            file_context = f"\n[Uploaded File Content:]\n{uploaded_file.getvalue().decode('utf-8')[:4000]}"

    st.markdown("---")
    st.markdown("### 🎭 Creative Writing Triggers:")
    st.write("- **Shayari:** *'ek line likho, automatic deep poetry banegi'*")
    st.write("- **Story:** *'thought dalo, complete novel layout ready'*")
    st.write("- **Song:** *'rap/lyrics ke liye concept type karein'*")

# Display Premium Chat Layout
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Main Chat Input (Universal Command Box)
if user_input := st.chat_input("Ask anything, search live data, generate HD photos, or type creative thoughts..."):
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.markdown(user_input)

    with st.chat_message("assistant"):
        response_placeholder = st.empty()
        
        # 🎨 AI IMAGE GENERATION ENGINE (Smart Intent Detection)
        image_keywords = ["image", "photo", "picture", "draw", "banao", "banado", "banaiye", "create", "generate"]
        is_image_request = any(keyword in user_input.lower() for keyword in image_keywords)

        if is_image_request:
            with st.spinner("🎨 AG ChatGPT is drawing your imagination in Ultra HD..."):
                try:
                    IMAGE_API_URL = "https://huggingface.co"
                    headers = {"Authorization": "Bearer hf_JdKxXvXvXvXvXvXvXvXvXvXvXvXvXvXv"}
                    
                    clean_prompt = user_input
                    for word in image_keywords + ["ki", "ko", "ek", "please", "of"]:
                        clean_prompt = clean_prompt.lower().replace(word, "").strip()
                    
                    if not clean_prompt: clean_prompt = user_input

                    img_response = requests.post(IMAGE_API_URL, headers=headers, json={"inputs": clean_prompt}, timeout=50)
                    
                    if img_response.status_code == 200:
                        st.image(img_response.content, caption=f"AI Artwork: {user_input}", use_container_width=True)
                        st.download_button(
                            label="📥 Download HD Image",
                            data=img_response.content,
                            file_name=f"ag_ai_{clean_prompt.replace(' ', '_')}.png",
                            mime="image/png"
                        )
                        full_response = "✨ Maine aapki command ke aadhar par High-Quality photo upar generate kar di hai. Aap use download button se save kar sakte hain!"
                        response_placeholder.markdown(full_response)
                        st.session_state.messages.append({"role": "assistant", "content": full_response})
                    else:
                        st.error("Image Engine limits reached. Please try after 10 seconds.")
                except Exception as e:
                    st.error(f"Image Error: {str(e)}")
        
        else:
            # 🌐 LIVE DEEP WEB SEARCH CRAWLER (2026 LIVE ENGINE)
            web_context = ""
            # Creative requests (like story, song, shayari) don't need web crawling delay
            creative_keywords = ["kahani", "story", "shayari", "poem", "kavita", "gana", "song", "lyrics", "rap"]
            is_creative_request = any(cw in user_input.lower() for cw in creative_keywords)

            if not is_creative_request:
                with st.spinner("🔍 Deep searching live internet servers for real-time 2026 data..."):
                    try:
                        with DDGS() as ddgs:
                            search_results = list(ddgs.text(f"{user_input} current updates 2026", max_results=3))
                            if search_results:
                                web_context += "\n".join([f"Info: {res['body']}" for res in search_results])
                            
                            news_results = list(ddgs.news(user_input, max_results=2))
                            if news_results:
                                web_context += "\n" + "\n".join([f"News [{res['date']}]: {res['title']} - {res['body']}" for res in news_results])
                    except:
                        pass

            # 🧠 CHATGPT MEGA MASTER PROMPT SYSTEM (With Creative Sub-Modules)
            system_prompt = (
                "You are AG ChatGPT Plus, an elite enterprise level AI assistant. "
                "Today is Friday, October 9, 2026. You possess world-class capabilities in professional writing, data search, coding, and artistic literature. "
                "CRITICAL CAPABILITIES:\n"
                "1. STORY MODE: If the user provides a thought, prompt, or incomplete plot line for a story ('kahani'), expand it into a rich, engaging, emotionally gripping, and well-structured story or novel layout.\n"
                "2. SHAYARI MODE: If the user provides an incomplete poetry line or theme ('shayari', 'kavita'), complete it with deep lyrical emotion, traditional meter/rhyme, and beautiful vocabulary.\n"
                "3. SONGWRITER MODE: If the user drops a beat idea, concept, or chorus line ('gana', 'lyrics', 'rap'), write structured song blocks complete with [Verse], [Chorus], and [Bridge].\n"
                "4. FOR GENERAL & LIVE SEARCH: Always analyze the 2026 live web data below to provide structural, up-to-date textbook level answers."
            )
            
            if web_context: 
                system_prompt += f"\n\n[REAL-TIME LIVE INTERNET DATA PIPELINE (2026):]\n{web_context}"
            if file_context: 
                system_prompt += f"\n\n[Uploaded Document/Company Data Context:]\n{file_context}"

            try:
                # Active streaming engine
                completion = client.chat.completions.create(
                    model=GROQ_MODEL,
                    messages=[
                        {"role": "system", "content": system_prompt},
                        {"role": "user", "content": user_input}
                    ],
                    stream=True, 
                )

                full_response = ""
                for chunk in completion:
                    if chunk.choices and chunk.choices[0].delta.content:
                        full_response += chunk.choices[0].delta.content
                        response_placeholder.markdown(full_response + "▌")
                
                response_placeholder.markdown(full_response)
                st.session_state.messages.append({"role": "assistant", "content": full_response})
                
            except Exception as e:
                st.error(f"Neural Engine Connection Error: {str(e)}")

    # 🎯 JAVASCRIPT HACK FOR AUTOMATIC DOWNWARD FOCUS (Instant View)
    components.html("""
        <script>
            window.parent.document.querySelector('section.main').scrollTo({
                top: window.parent.document.querySelector('section.main').scrollHeight,
                behavior: 'smooth'
            });
        </script>
    """, height=0)
