import os
import streamlit as st
from google import genai
from google.genai import types

# ---------------------------------------------------------
# 1. Page Configuration
# ---------------------------------------------------------
st.set_page_config(
    page_title="LEARN WITH SHAFIQ - All-in-One AI Suite",
    page_icon="🎓",
    layout="wide",
)

# App Header
st.title("🎓 LEARN WITH SHAFIQ - Multi-AI Suite")
st.write("Pakistani Students ke liye All-in-One AI Learning & Media Toolkit")

# ---------------------------------------------------------
# 2. Security & Client Setup
# ---------------------------------------------------------
api_key = os.environ.get("GEMINI_API_KEY")

if not api_key:
    st.error("Please set your GEMINI_API_KEY in Streamlit Secrets to proceed.")
    st.stop()

client = genai.Client(api_key=api_key)

# ---------------------------------------------------------
# 3. Sidebar Tool Selection
# ---------------------------------------------------------
st.sidebar.header("🛠️ Choose AI Model/Tool")
selected_tool = st.sidebar.selectbox(
    "Aap konsa AI tool istemal karna chahte hain?",
    [
        "📚 Text Assistant (Gemini 3.6 Flash)",
        "🎨 Image Generator (Imagen 3)",
        "🎥 Video Generator (Veo 2)",
        "🎙️ Speech & Music Assistant"
    ]
)

# ---------------------------------------------------------
# TOOL 1: TEXT CHATBOT (GEMINI 3.6 FLASH)
# ---------------------------------------------------------
if selected_tool == "📚 Text Assistant (Gemini 3.6 Flash)":
    st.subheader("📚 AI Study Assistant & MCQ Generator")
    
    SYSTEM_INSTRUCTION = """
    You are the official AI Study Assistant for 'LEARN WITH SHAFIQ'.
    Help Pakistani students excel in FPSC, SPSC, NTS, STS, PTS, BPSC, KPSC, and board exams.
    Provide accurate notes, formatted MCQs with 4 options, and clear educational breakdowns.
    """

    if "messages" not in st.session_state:
        st.session_state.messages = []

    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    if prompt := st.chat_input("Sawal poochein, notes banwayein ya MCQs generate karein..."):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        with st.chat_message("assistant"):
            with st.spinner("Jawab taiyar ho raha hai..."):
                try:
                    response = client.models.generate_content(
                        model="gemini-3.6-flash",
                        contents=prompt,
                        config=types.GenerateContentConfig(
                            system_instruction=SYSTEM_INSTRUCTION,
                            temperature=0.3,
                        ),
                    )
                    answer = response.text
                    st.markdown(answer)
                    st.session_state.messages.append({"role": "assistant", "content": answer})
                except Exception as e:
                    st.error(f"Error generating text response: {e}")

# ---------------------------------------------------------
# TOOL 2: IMAGE GENERATION (IMAGEN 3)
# ---------------------------------------------------------
elif selected_tool == "🎨 Image Generator (Imagen 3)":
    st.subheader("🎨 AI Image & Educational Diagram Generator")
    st.write("Apne subject ke mutaliq koi bhi diagram ya image generate karein.")

    img_prompt = st.text_area(
        "Image ki tafseel (Prompt) likhein:",
        placeholder="e.g., A detailed labeled diagram of human cell structure, high quality educational illustration"
    )

    if st.button("Generate Image 🖼️"):
        if not img_prompt:
            st.warning("Pehle prompt likhein.")
        else:
            with st.spinner("Image ban rahi hai (kuch seconds intezar karein)..."):
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
                except Exception as e:
                    st.error(f"Error generating image: {e}")

# ---------------------------------------------------------
# TOOL 3: VIDEO GENERATION (VEO 2)
# ---------------------------------------------------------
elif selected_tool == "🎥 Video Generator (Veo 2)":
    st.subheader("🎥 AI Educational Video Generator (Veo)")
    st.info("Note: Video generation mein 1-2 minute lag sakte hain.")

    vid_prompt = st.text_area(
        "Video Prompt likhein:",
        placeholder="e.g., 3D animation showing water cycle with rain falling on mountains"
    )

    if st.button("Generate Video 🎬"):
        if not vid_prompt:
            st.warning("Pehle video prompt likhein.")
        else:
            with st.spinner("AI Video banai ja rahi hai (isme time lagega)..."):
                try:
                    # Request video generation (Google Cloud billing enabled key required)
                    operation = client.models.generate_videos(
                        model="veo-2.0-generate-001",
                        prompt=vid_prompt,
                        config=types.GenerateVideosConfig(
                            person_generation="dont_allow",
                            aspect_ratio="16:9",
                            duration_seconds=5
                        ),
                    )
                    st.success("Video request submit ho gayi hai!")
                except Exception as e:
                    st.error(f"Error generating video: {e}\n(Make sure Google Cloud Billing is enabled for Veo models).")

# ---------------------------------------------------------
# TOOL 4: SPEECH & AUDIO ASSISTANT
# ---------------------------------------------------------
elif selected_tool == "🎙️ Speech & Music Assistant":
    st.subheader("🎙️ Voice & Audio Companion")
    st.write("Audio generation aur Live Speech processing tools.")
    st.info("Multimodal Voice Live API features coming soon to this section.")
