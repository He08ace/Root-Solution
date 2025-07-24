import streamlit as st
import requests
import io
from docx import Document
import base64

# Set page config
st.set_page_config(page_title="Audiobook TTS Reader", layout="centered")

st.title("📖 Audiobook TTS Reader")
st.markdown("Turn text or chapters into audio using ElevenLabs voices.")

# Sidebar for API key and voice selection
st.sidebar.header("🔧 Settings")
api_key = st.sidebar.text_input(ELEVENLABS_API_KEY = "sk_d58c4c8cf3e18fece726e6664db6f9efae76ed2de3cb893c")

# Get available voices
def get_voices(api_key):
    headers = {
        "xi-api-key": api_key
    }
    response = requests.get("https://api.elevenlabs.io/v1/voices", headers=headers)
    if response.status_code == 200:
        voices = response.json().get("voices", [])
        return {voice["name"]: voice["voice_id"] for voice in voices}
    return {}

voices = get_voices(api_key) if api_key else {}
voice_names = list(voices.keys()) if voices else []

# Text input or file upload
st.subheader("Step 1: Input your content")
text_input = st.text_area("✍️ Paste your text here", height=200)

uploaded_file = st.file_uploader("📄 Or upload a .txt or .docx file", type=["txt", "docx"])
file_text = ""

if uploaded_file:
    try:
        if uploaded_file.name.endswith(".txt"):
            file_text = uploaded_file.read().decode("utf-8")
        elif uploaded_file.name.endswith(".docx"):
            doc = Document(uploaded_file)
            file_text = "\n".join([para.text for para in doc.paragraphs])
    except Exception as e:
        st.error(f"Error reading file: {e}")

# Choose source text
text = text_input or file_text

if text:
    st.subheader("Step 2: Choose Voice")
    if not voices:
        st.warning("⚠️ Please enter a valid ElevenLabs API key in the sidebar.")
    else:
        selected_voice_name = st.selectbox("🎤 Choose a voice", voice_names)
        selected_voice_id = voices[selected_voice_name]

        if st.button("▶️ Generate Audio"):
            with st.spinner("Generating audio..."):
                headers = {
                    "xi-api-key": api_key,
                    "Content-Type": "application/json"
                }
                payload = {
                    "text": text,
                    "model_id": "eleven_monolingual_v1",
                    "voice_settings": {
                        "stability": 0.5,
                        "similarity_boost": 0.75
                    }
                }

                response = requests.post(
                    f"https://api.elevenlabs.io/v1/text-to-speech/{selected_voice_id}",
                    headers=headers,
                    json=payload
                )

                if response.status_code == 200:
                    audio_bytes = response.content
                    st.audio(audio_bytes, format="audio/mp3")

                    # Download link
                    b64 = base64.b64encode(audio_bytes).decode()
                    href = f'<a href="data:audio/mp3;base64,{b64}" download="audiobook.mp3">💾 Download MP3</a>'
                    st.markdown(href, unsafe_allow_html=True)
                else:
                    st.error(f"⚠️ Failed to generate audio: {response.status_code} - {response.text}")
else:
    st.warning("⚠️ Please upload a file or enter some text.")
