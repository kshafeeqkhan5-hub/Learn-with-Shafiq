import os
import streamlit as st
import google.generativeai as genai

st.set_page_config(page_title="LEARN WITH SHAFIQ", page_icon="🎓")
st.title("🎓 LEARN WITH SHAFIQ")

api_key = st.secrets.get("GEMINI_API_KEY") or os.environ.get("GEMINI_API_KEY")

if not api_key:
    st.error("⚠️ GEMINI_API_KEY missing hai!")
    st.stop()

api_key = str(api_key).strip().strip('"').strip("'")

# Configure client
genai.configure(api_key=api_key)

if prompt := st.chat_input("Ask anything..."):
    st.chat_message("user").markdown(prompt)
    with st.chat_message("assistant"):
        try:
            # Using v1beta model endpoint
            model = genai.GenerativeModel('gemini-1.5-flash')
            response = model.generate_content(prompt)
            st.markdown(response.text)
        except Exception as e:
            st.error(f"❌ Error: {e}")
