import os
import streamlit as st
from google import genai
from google.genai import types

st.set_page_config(
    page_title="LEARN WITH SHAFIQ - AI Study Assistant",
    page_icon="🎓",
    layout="wide",
)

st.title("🎓 LEARN WITH SHAFIQ")
st.subheader("Your Personal AI Study Companion for Pakistani Students")
st.write(
    "Ask anything about General Knowledge, Pakistan Affairs, Islamiyat, Science, Competitive Exam Test Prep (FPSC, SPSC, NTS, STS), or General Notes!"
)

# Fetch API Key cleanly
api_key = st.secrets.get("GEMINI_API_KEY") or os.environ.get("GEMINI_API_KEY")

if not api_key:
    st.error("⚠️ GEMINI_API_KEY missing hai! Streamlit Cloud ke Secrets mein API key save karein.")
    st.stop()

# Strip any accidental whitespace/newlines
api_key = api_key.strip()

# Explicitly pass api_key to Client
client = genai.Client(api_key=api_key)

st.sidebar.header("🛠️ Choose Tool Mode")
mode = st.sidebar.radio(
    "Select Assistant Mode:",
    ["📚 Study Chatbot (Text / Notes / MCQs)", "🎨 AI Image Generator"]
)

SYSTEM_INSTRUCTION = """
You are the official AI Study Assistant for the platform 'LEARN WITH SHAFIQ'. 
Your goal is to help Pakistani students excel in their studies, school exams, board exams, and competitive job testing services (such as FPSC, SPSC, NTS, STS, PTS, BPSC, KPSC).
"""

if mode == "📚 Study Chatbot (Text / Notes / MCQs)":
    if "messages" not in st.session_state:
        st.session_state.messages = []

    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    if prompt := st.chat_input("Ask a question, request study notes, or generate MCQs..."):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        with st.chat_message("assistant"):
            with st.spinner("Searching knowledge base..."):
                response_text = None
                last_error = None
                
                # Active standard models
                models_to_try = ["gemini-2.5-flash", "gemini-1.5-flash"]
                
                for model_name in models_to_try:
                    try:
                        response = client.models.generate_content(
                            model=model_name,
                            contents=prompt,
                            config=types.GenerateContentConfig(
                                system_instruction=SYSTEM_INSTRUCTION,
                                temperature=0.3,
                            ),
                        )
                        if response and response.text:
                            response_text = response.text
                            break
                    except Exception as e:
                        last_error = str(e)
                        continue

                if response_text:
                    st.markdown(response_text)
                    st.session_state.messages.append({"role": "assistant", "content": response_text})
                else:
                    st.error(f"API Error Details: {last_error}")

elif mode == "🎨 AI Image Generator":
    st.markdown("### 🖼️ Educational Image Generator")
    img_prompt = st.text_area("Image description likhein:")
    if st.button("Generate Image"):
        st.info("Text Chatbot mode use karein!")
