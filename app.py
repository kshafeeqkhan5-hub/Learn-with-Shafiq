import os
import streamlit as st
from google import genai
from google.genai import types

# Set up Streamlit Page Configuration
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

# Access API key securely from environment/secrets
api_key = os.environ.get("GEMINI_API_KEY")

if not api_key:
    st.error(
        "Please set your GEMINI_API_KEY environment variable to proceed."
    )
    st.stop()

client = genai.Client(api_key=api_key)

# System Prompt to instruct the AI persona
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

# Initialize Chat History in Streamlit session
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display previous messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# User Input Prompt
if prompt := st.chat_input(
    "Ask a question, request study notes, or generate MCQs..."
):
    # Display user query
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Generate response from Gemini API
    with st.chat_message("assistant"):
        with st.spinner("Searching knowledge base..."):
            try:
                response = client.models.generate_content(
                    model="model="gemini-2.5-flash",
                    contents=prompt,
                    config=types.GenerateContentConfig(
                        system_instruction=SYSTEM_INSTRUCTION,
                        temperature=0.3,
                    ),
                )
                answer = response.text
                st.markdown(answer)
                st.session_state.messages.append(
                    {"role": "assistant", "content": answer}
                )
            except Exception as e:
                st.error(f"Error generating response: {e}")
