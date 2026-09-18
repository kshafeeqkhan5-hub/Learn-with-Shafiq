import os
import streamlit as st
from openai import OpenAI

st.set_page_config(page_title="LEARN WITH SHAFIQ", page_icon="🎓")
st.title("🎓 LEARN WITH SHAFIQ")
st.caption("Your Personal AI Study Companion for Competitive Exams")

# Retrieve OpenRouter Key from Secrets
api_key = st.secrets.get("OPENROUTER_API_KEY") or os.environ.get("OPENROUTER_API_KEY")

if not api_key:
    st.error("⚠️ Secrets mein OPENROUTER_API_KEY missing hai!")
    st.stop()

# Initialize OpenRouter Client
client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=str(api_key).strip(),
)

if "messages" not in st.session_state:
    st.session_state.messages = []

for msg in st.session_state.messages:
    st.chat_message(msg["role"]).markdown(msg["content"])

if prompt := st.chat_input("Ask anything about exams, syllabus, GK..."):
    st.chat_message("user").markdown(prompt)
    st.session_state.messages.append({"role": "user", "content": prompt})

    with st.chat_message("assistant"):
        try:
            # Universal dynamic free model endpoint
            response = client.chat.completions.create(
                model="openrouter/free",
                messages=[
                    {"role": m["role"], "content": m["content"]}
                    for m in st.session_state.messages
                ]
            )
            answer = response.choices[0].message.content
            st.markdown(answer)
            st.session_state.messages.append({"role": "assistant", "content": answer})
        except Exception as e:
            st.error(f"❌ Error: {e}")
