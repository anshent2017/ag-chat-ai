def universal_data_crawler(query_text):
    context = ""
    query_lower = query_text.lower()
    if yf and ("stock" in query_lower or "price" in query_lower or "share" in query_lower):
        try:
            words = query_text.upper().split()
            for word in words:
                if len(word) <= 5 and word.isalpha():
                    info = yf.Ticker(word).history(period="1d")
                    if not info.empty:
                        context += f"\n- Live Finance ({word}): Closing Price ${info['Close'].iloc[-1]:.2f}"
                        break
        except: pass
    if wikipediaapi and len(query_text.split()) < 4:
        try:
            page = wikipediaapi.Wikipedia('AG_Universal_Bot/1.0', 'en').page(query_text)
            if page.exists(): context += f"\n- Wikipedia: {page.summary[:500]}"
        except: pass
    try:
        encoded_query = urllib.parse.quote(query_text)
        res = requests.get(f"https://duckduckgo.com{encoded_query}", headers={'User-Agent': 'Mozilla/5.0'}, timeout=10)
        if res.status_code == 200 and BeautifulSoup:
            links = BeautifulSoup(res.text, 'html.parser').find_all('a', class_='result__snippet')
            if links: context += "\n" + "\n".join([f"- Live Source: {l.text.strip()}" for l in links[:3]])
    except: pass
    return context

incoming_payload = st.query_params.get("voice_input_payload", "")

if incoming_payload:
    st.query_params.clear()
    st.session_state.messages.append({"role": "user", "content": incoming_payload})
    with st.spinner("🔍 Scanning Global Web..."):
        web_context = universal_data_crawler(incoming_payload)
        sys_prompt = "You are AG ChatGPT Plus. Combine live web data below with your knowledge."
        if web_context: sys_prompt += f"\n\n[LIVE DATA:]\n{web_context}"
        try:
            comp = client.chat.completions.create(model=GROQ_MODEL, messages=[{"role": "system", "content": sys_prompt}, {"role": "user", "content": incoming_payload}], stream=True)
            full_res = ""
            for chunk in comp:
                if chunk.choices[0].delta.content: full_res += chunk.choices[0].delta.content
            st.session_state.messages.append({"role": "assistant", "content": full_res})
        except Exception as e: st.session_state.messages.append({"role": "assistant", "content": f"Error: {e}"})
    st.rerun()

else:
    text_box_input = st.chat_input("Ask AG ChatGPT anything (A-Z Search, Finance Analytics)...")
    if text_box_input:
        st.session_state.messages.append({"role": "user", "content": text_box_input})
        with st.chat_message("user"): st.markdown(text_box_input)
        with st.chat_message("assistant"):
            resp_placeholder = st.empty()
            with st.spinner("🔍 Scanning Global Web..."):
                web_context = universal_data_crawler(text_box_input)
                sys_prompt = "You are AG ChatGPT Plus. Combine live web data below with your knowledge."
                if web_context: sys_prompt += f"\n\n[LIVE DATA:]\n{web_context}"
            try:
                comp = client.chat.completions.create(model=GROQ_MODEL, messages=[{"role": "system", "content": sys_prompt}, {"role": "user", "content": text_box_input}], stream=True)
                full_res = ""
                for chunk in comp:
                    if chunk.choices[0].delta.content:
                        full_res += chunk.choices[0].delta.content
                        resp_placeholder.markdown(full_res + "▌")
                resp_placeholder.markdown(full_res)
                st.session_state.messages.append({"role": "assistant", "content": full_res})
            except Exception as e: st.error(f"Error: {e}")
