import os
import streamlit as st
import google.generativeai as genai

# Page Configuration
st.set_page_config(
    page_title="LEARN WITH SHAFIQ - AI Study Assistant",
    page_icon="🎓",
    layout="wide",
)

# App Header
st.title("🎓 LEARN WITH SHAFIQ")
st.subheader("Your Personal AI Study Companion for Pakistani Students")
st.write(
    "Ask anything about General Knowledge, Pakistan Affairs, Islamiyat, Science, Competitive Exam Test Prep (FPSC, SPSC, NTS, STS), or General Notes!"
)

# Fetch API Key securely
api_key = st.secrets.get("GEMINI_API_KEY") or os.environ.get("GEMINI_API_KEY")

if not api_key:
    st.error("⚠️ GEMINI_API_KEY missing hai! Streamlit Secrets mein API key add karein.")
    st.stop()

# Configure Gemini API
genai.configure(api_key=api_key)

# Sidebar Selection
st.sidebar.header("🛠️ Choose Tool Mode")
mode = st.sidebar.radio(
    "Select Assistant Mode:",
    ["📚 Study Chatbot (Text / Notes / MCQs)", "🎨 AI Image Generator"]
)

# SYSTEM INSTRUCTION FOR CHATBOT
SYSTEM_INSTRUCTION = """
You are the official AI Study Assistant for 'LEARN WITH SHAFIQ'.
Help Pakistani students prepare for school/board exams and competitive job tests (FPSC, SPSC, NTS, STS, PTS).
Provide clear, well-structured, easy-to-read notes and MCQs with answer keys.
"""

# MODE 1: CHATBOT
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
            with st.spinner("Response generate ho raha hai..."):
                response_text = None
                
                # Active stable models
                fallback_models = ['gemini-1.5-flash', 'gemini-1.5-pro']
                
                for model_name in fallback_models:
                    try:
                        model = genai.GenerativeModel(
                            model_name=model_name,
                            system_instruction=SYSTEM_INSTRUCTION
                        )
                        res = model.generate_content(prompt)
                        if res and res.text:
                            response_text = res.text
                            break
                    except Exception as e:
                        continue

                if response_text:
                    st.markdown(response_text)
                    st.session_state.messages.append({"role": "assistant", "content": response_text})
                else:
                    st.error("API Connection Fail. Check karein ke Google AI Studio se 'GEMINI_API_KEY' active hai ya nahi.")

# MODE 2: IMAGE GENERATOR
elif mode == "🎨 AI Image Generator":
    st.markdown("### 🖼️ Educational Image Generator")
    img_prompt = st.text_area("Image description likhein:")
    
    if st.button("Generate Image"):
        st.info("Direct Image Generation feature requires a paid Imagen tier. Please use text mode for study material!")
