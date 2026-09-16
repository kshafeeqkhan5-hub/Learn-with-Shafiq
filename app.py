import os
import streamlit as st
from google import genai
from google.genai import types

st.set_page_config(page_title="LEARN WITH SHAFIQ", page_icon="🎓")
st.title("🎓 LEARN WITH SHAFIQ")

api_key = st.secrets.get("GEMINI_API_KEY") or os.environ.get("GEMINI_API_KEY")

if not api_key:
    st.error("⚠️ Secrets mein GEMINI_API_KEY missing hai!")
    st.stop()

api_key = str(api_key).strip().strip('"').strip("'")

try:
    client = genai.Client(api_key=api_key)
    st.success("✅ API Key successfully loaded!")
except Exception as e:
    st.error(f"❌ Client Initialization Error: {e}")
    st.stop()

if prompt := st.chat_input("Ask anything..."):
    st.chat_message("user").markdown(prompt)
    with st.chat_message("assistant"):
        try:
            response = client.models.generate_content(
                model="gemini-2.5-flash",
                contents=prompt
            )
            st.markdown(response.text)
        except Exception as e:
            st.error(f"❌ Direct API Error Details:\n\n{e}")
