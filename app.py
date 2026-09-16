import os
import streamlit as st
from google import genai
from google.genai import types

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

# Access API key securely from Streamlit Secrets or Environment
api_key = st.secrets.get("GEMINI_API_KEY") or os.environ.get("GEMINI_API_KEY")

if not api_key:
    st.error("⚠️ GEMINI_API_KEY missing hai! Streamlit Cloud ke Secrets mein API key save karein.")
    st.stop()

# Initialize Gemini Client
client = genai.Client(api_key=api_key)

# Sidebar Menu Selection
st.sidebar.header("🛠️ Choose Tool Mode")
mode = st.sidebar.radio(
    "Select Assistant Mode:",
    ["📚 Study Chatbot (Text / Notes / MCQs)", "🎨 AI Image Generator"]
)

# System Prompt
SYSTEM_INSTRUCTION = """
You are the official AI Study Assistant for the platform 'LEARN WITH SHAFIQ'. 
Your goal is to help Pakistani students excel in their studies, school exams, board exams, and competitive job testing services (such as FPSC, SPSC, NTS, STS, PTS, BPSC, KPSC).

Guidelines:
1. Provide accurate, clear, and easy-to-understand educational responses.
2. Format notes with clear bullet points, bold key terms, and structured headings.
3. When requested for test MCQs, present questions clearly with 4 options and provide an answer key at the end.
4. Maintain an encouraging, helpful, and respectful tone for students.
5. If students ask in Roman Urdu or English, respond in clear English (or a mix if explicitly asked).
"""

# MODE 1: STUDY CHATBOT
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
                
                # Active models to try in sequence
                models_to_try = ["gemini-2.5-flash", "gemini-2.5-pro", "gemini-1.5-flash"]
                
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
                    except Exception:
                        continue

                if response_text:
                    st.markdown(response_text)
                    st.session_state.messages.append({"role": "assistant", "content": response_text})
                else:
                    st.error("API response fail ho raha hai. Secrets mein GEMINI_API_KEY confirm karein.")

# MODE 2: IMAGE GENERATOR
elif mode == "🎨 AI Image Generator":
    st.markdown("### 🖼️ Educational Image Generator")
    img_prompt = st.text_area("Image description likhein:")
    
    if st.button("Generate Image"):
        if not img_prompt:
            st.warning("Please enter a description first.")
        else:
            with st.spinner("Processing image request..."):
                try:
                    result = client.models.generate_images(
                        model='imagen-3.0-generate-002',
                        prompt=img_prompt,
                        config=types.GenerateImagesConfig(
                            number_of_images=1,
                            aspect_ratio="1:1",
                            output_mime_type="image/jpeg"
                        )
                    )
                    for generated_image in result.generated_images:
                        st.image(generated_image.image.image_bytes, caption=img_prompt, use_column_width=True)
                except Exception:
                    st.error("Image generation key restriction ki wajah se block hai. Text Chatbot mode bilkul sahi chalega!")
