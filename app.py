if user_input:
    st.session_state.messages.append({"role": "user", "content": user_input})
    
    with st.chat_message("user"):
        st.markdown(user_input)
        
    query_lower = user_input.lower()
    is_image_request = any(word in query_lower for word in ["photo", "image", "बनाओ", "banao", "generate", "picture"])
    
    if is_image_request:
        with st.chat_message("assistant"):
            with st.spinner("🎨 AG AI Image Studio: Generating HD Photo..."):
                try:
                    encoded_prompt = urllib.parse.quote(user_input)
                    image_url = f"https://pollinations.ai{encoded_prompt}?width=1024&height=1024&nologo=true"
                    st.markdown(f"### 🎨 Generated Photo for: *\"{user_input}\"*")
                    st.image(image_url, use_container_width=True)
                    st.session_state.messages.append({
                        "role": "assistant", 
                        "content": f"📸 **Generated Photo for:** *\"{user_input}\"*\n\n<img src='{image_url}' width='100%' style='border-radius:10px;'/>"
                    })
                except Exception as img_err:
                    st.error(f"Image Studio Error: {str(img_err)}")
                        
    elif uploaded_file:
        with st.chat_message("assistant"):
            with st.spinner("🧠 AG Vision Engine: Analyzing uploaded media..."):
                try:
                    base64_image = encode_image_to_base64(uploaded_file)
                    headers = {
                        "Authorization": f"Bearer {GROQ_API_KEY}",
                        "Content-Type": "application/json"
                    }
                    payload = {
                        "model": GROQ_VISION_MODEL,
                        "messages": [
                            {
                                "role": "user",
                                "content": [
                                    {"type": "text", "text": f"The user asks: {user_input}. Look at the attached image carefully and answer comprehensively in Hindi or English."},
                                    {
                                        "type": "image_url",
                                        "image_url": {
                                            "url": f"data:image/jpeg;base64,{base64_image}"
                                        }
                                    }
                                ]
                            }
                        ],
                        "stream": False
                    }
                    
                    api_url = "https://groq.com"
                    res = requests.post(api_url, json=payload, headers=headers, timeout=30)
                    
                    if res.status_code == 200:
                        full_response = res.json()['choices'][0]['message']['content']
                        st.markdown(full_response)
                        st.session_state.messages.append({"role": "assistant", "content": full_response})
                    else:
                        st.error(f"Vision API Error Code {res.status_code}: {res.text}")
                except Exception as vision_err:
                    st.error(f"Vision Engine Connection Error: {str(vision_err)}")
                        
    else:
        # ✅ फ़िक्स: यहाँ पूरे ब्लॉक को मुख्य 'if user_input:' के 'else' भाग के रूप में 4 स्पेस आगे इंडेंट किया गया है
        with st.chat_message("assistant"):
            with st.spinner("🔍 Deep searching live internet servers..."):
                web_context = fetch_global_and_social_search(user_input)
                system_prompt = (
                    "You are AG ChatGPT Plus, a world-class autonomous AI collaborator. "
                    "Today's date is verified as Saturday, October 10, 2026. "
                    "Always combine the live global search data below with your neural networks to frame highly comprehensive responses."
                )
                if web_context: 
                    system_prompt += f"\n\n[UNIVERSAL LIVE WEB PIPELINE DATA (2026):]\n{web_context}"
                    
            try:
                headers = {
                    "Authorization": f"Bearer {GROQ_API_KEY}",
                    "Content-Type": "application/json"
                }
                payload = {
                    "model": GROQ_TEXT_MODEL,
                    "messages": [
                        {"role": "system", "content": system_prompt},
                        {"role": "user", "content": user_input}
                    ],
                    "stream": False
                }
                
                # ✅ फ़िक्स: अमान्य होस्ट "groq.com" को बदलकर सटीक लाइव एपीआई एंडपॉइंट पाथ किया गया
                api_url = "https://groq.com"
                res = requests.post(api_url, json=payload, headers=headers, timeout=30)
                
                if res.status_code == 200:
                    full_response = res.json()['choices'][0]['message']['content']
                    st.markdown(full_response)
                    st.session_state.messages.append({"role": "assistant", "content": full_response})
                else:
                    st.error(f"Core API Error Code {res.status_code}: {res.text}")
                    
            except Exception as e:
                error_msg = f"Neural Engine Connection Error: {str(e)}"
                st.error(error_msg)
                st.session_state.messages.append({"role": "assistant", "content": error_msg})
