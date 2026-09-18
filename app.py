import os
import requests
import streamlit as st

st.set_page_config(page_title="LEARN WITH SHAFIQ", page_icon="🎓")
st.title("🎓 LEARN WITH SHAFIQ")
st.caption("Your Personal AI Study Companion for Pakistani Students")

# Retrieve API Key from Secrets
api_key = st.secrets.get("GEMINI_API_KEY") or os.environ.get("GEMINI_API_KEY")

if not api_key:
    st.error("⚠️ Secrets mein GEMINI_API_KEY missing hai!")
    st.stop()

# Clean key text
api_key = str(api_key).strip().strip('"').strip("'")

# Chat memory state
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display previous messages
for msg in st.session_state.messages:
    st.chat_message(msg["role"]).markdown(msg["content"])

# User Input
if prompt := st.chat_input("Ask anything about exams, syllabus, GK..."):
    st.chat_message("user").markdown(prompt)
    st.session_state.messages.append({"role": "user", "content": prompt})

    with st.chat_message("assistant"):
        # REST API Endpoint URL
        url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={api_key}"
        
        headers = {"Content-Type": "application/json"}
        payload = {
            "contents": [{
                "parts": [{"text": prompt}]
            }]
        }

        try:
            response = requests.post(url, json=payload, headers=headers)
            res_data = response.json()

            if response.status_code == 200:
                answer = res_data["candidates"][0]["content"]["parts"][0]["text"]
                st.markdown(answer)
                st.session_state.messages.append({"role": "assistant", "content": answer})
            else:
                error_msg = res_data.get("error", {}).get("message", "Unknown Error")
                st.error(f"❌ API Error ({response.status_code}): {error_msg}")

        except Exception as e:
            st.error(f"❌ Connection Error: {e}")
