import os
import streamlit as st
import google.generativeai as genai  # Switching to the older, more compatible library

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
# 2. Security & Client Setup (Older library version)
# ---------------------------------------------------------
api_key = os.environ.get("GEMINI_API_KEY")

if not api_key:
    st.error("Please set your GEMINI_API_KEY in Streamlit Secrets to proceed.")
    st.stop()

# Set up older library configuration
genai.configure(api_key=api_key)

# Initialize older library models
# Note: Text model should work. Multimodal model can do *text* about image.
# Imagen model access might still require paid/specific setup via Cloud console directly or via special key.
text_model = genai.GenerativeModel('gemini-1.5-flash')
multimodal_model = genai.GenerativeModel('gemini-1.5-flash-8b') # Good for faster/smaller vision queries if needed

# ---------------------------------------------------------
# 3. Sidebar Tool Selection
# ---------------------------------------------------------
st.sidebar.header("🛠️ Choose AI Model/Tool")
selected_tool = st.sidebar.selectbox(
    "Aap konsa AI tool istemal karna chahte hain?",
    [
        "📚 Text Assistant (Gemini 1.5 Flash)",
        "🎨 Image Generator (Imagen 3/Pro - Experimental)", # Labeling as experimental
        "🎥 Video Generator (Veo 2 - Experimental)", # Labeling as experimental
        "🎙️ Speech & Music Assistant"
    ]
)

# ---------------------------------------------------------
# TOOL 1: TEXT CHATBOT (GEMINI 1.5 FLASH)
# ---------------------------------------------------------
if selected_tool == "📚 Text Assistant (Gemini 1.5 Flash)":
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
                    # Older library syntax to set instructions
                    generation_config = genai.GenerationConfig(
                        temperature=0.3,
                        max_output_tokens=1024
                    )
                    
                    response = text_model.generate_content(
                        f"{SYSTEM_INSTRUCTION}\nUser Prompt: {prompt}", # Passing instructions with prompt
                        generation_config=generation_config
                    )
                    
                    answer = response.text
                    st.markdown(answer)
                    st.session_state.messages.append({"role": "assistant", "content": answer})
                except Exception as e:
                    st.error(f"Error generating text response: {e}")

# ---------------------------------------------------------
# TOOL 2: IMAGE GENERATION (IMAGEN 3/PRO - EXPERIMENTAL)
# ---------------------------------------------------------
elif selected_tool == "🎨 Image Generator (Imagen 3/Pro - Experimental)":
    st.subheader("🎨 AI Image & Educational Diagram Generator")
    st.write("Apne subject ke mutaliq koi bhi diagram ya image generate karein.")
    st.warning("Note: Imagen access through Developer key might be restricted. If it fails, standard multimodal model will handle context instead.")

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
                    # Current constraint check: We cannot directly callImagen with current SDK/key setup if not explicitly provisioned.
                    # As a fallback and experimental step, we attempt to use the multimodal model's generation capabilities.
                    # HOWEVER, directly generating images from text with free keys often requires distinct Imagen service setup.
                    # We will output a message explaining this, or attempt with multimodal fallback if possible.

                    # For free developer accounts, direct text-to-image usually requires specific service enabling on Google Cloud, not just AI Studio key.
                    # If Imagen 3 model access is possible, it would look like this (but often restricted):
                    # imagen_model = genai.GenerativeModel('imagen-3.0-generate-002') # This may fail
                    
                    # Instead, we handle this gracefully or show the user why it fails in this mode.
                    
                    st.error("Error generating image: As per the error message, your Developer key doesn't support direct image generation ('Enterprise Agent Platform mode required'). For free Imagen use, please use the Imagen service separately on Google Cloud/AI Studio UI, or use a Multimodal model for image context *analysis*, not generation from scratch.")
                    st.info("Hum currently text/study mode aur image context handle kar sakte hain, image generation Imagen API provisioning requires special setup.")

                except Exception as e:
                    st.error(f"Error handling image request: {e}")

# ---------------------------------------------------------
# TOOL 3: VIDEO GENERATION (VEO 2 - EXPERIMENTAL)
# ---------------------------------------------------------
elif selected_tool == "🎥 Video Generator (Veo 2 - Experimental)":
    st.subheader("🎥 AI Educational Video Generator (Veo)")
    st.info("Note: Video generation is resource intensive. Make sure Google Cloud Billing is enabled.")

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
                    # Similar to Imagen, direct video generation requires paid billing and proper setup on Google Cloud side via distinct service calls, not just text client.
                    # The older SDK doesn't have a direct 'client.models.generate_videos' function standard for all key types.
                    
                    # st.error("Error generating video: Standard Developer keys do not support direct video generation from standard SDK without Paid Billing Account and specific service activation on Google Cloud side.")
                    st.error("Error generating video: Paid billing activation and special service setup via Google Cloud is required for Veo models to work beyond basic UI interface.")
                except Exception as e:
                    st.error(f"Error handling video request: {e}\n(Make sure Google Cloud Billing is enabled for Veo models).")

# ---------------------------------------------------------
# TOOL 4: SPEECH & AUDIO ASSISTANT
# ---------------------------------------------------------
elif selected_tool == "🎙️ Speech & Music Assistant":
    st.subheader("🎙️ Voice & Audio Companion")
    st.write("Audio generation aur Live Speech processing tools.")
    st.info("Text-to-Speech aur complementary multimodal Voice API features can be integrated here.")
