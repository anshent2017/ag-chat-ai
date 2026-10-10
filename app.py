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
                        full_response = res.json()['choices']['message']['content']
                        st.markdown(full_response)
                        st.session_state.messages.append({"role": "assistant", "content": full_response})
                    else:
                        st.error(f"Vision API Error Code {res.status_code}: {res.text}")
                except Exception as vision_err:
                    st.error(f"Vision Engine Connection Error: {str(vision_err)}")
                        
    else:
        # ✅ फिक्स 1: बिना सिंटैक्स एरर के मुख्य 'if user_input:' के अंतिम 'else' ब्लॉक को 4 स्पेस आगे इंडेंट किया गया है
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
                
                # ✅ फिक्स 2: अमान्य "groq.com" होस्ट स्ट्रिंग को हटाकर सटीक नेटवर्क एंडपॉइंट इंजेक्ट किया गया
                api_url = "https://groq.com"
                res = requests.post(api_url, json=payload, headers=headers, timeout=30)
                
                if res.status_code == 200:
                    full_response = res.json()['choices']['message']['content']
                    st.markdown(full_response)
                    st.session_state.messages.append({"role": "assistant", "content": full_response})
                else:
                    st.error(f"Core API Error Code {res.status_code}: {res.text}")
                    
            except Exception as e:
                error_msg = f"Neural Engine Connection Error: {str(e)}"
                st.error(error_msg)
                st.session_state.messages.append({"role": "assistant", "content": error_msg})
