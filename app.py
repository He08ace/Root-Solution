import streamlit as st
import requests
from pydub import AudioSegment
import io
import docx

# Set your ElevenLabs API key here
ELEVENLABS_API_KEY = "your-api-key-here"  # Replace this with your actual API key

# Available voices from ElevenLabs (you can add more)
ELEVENLABS_VOICES = {
    "Rachel": "21m00Tcm4TlvDq8ikWAM",
    "Domi": "AZnzlk1XvdvUeBnXmlld",
    "Bella": "EXAVITQu4vr4xnSDxMaL",
    "Antoni": "ErXwobaYiN019PkySvjV",
    "Elli": "MF3mGyEYCl7XYWbV9V6O"
}

# Streamlit page setup
st.set_page_config(page_title="Audiobook TTS Reader", layout="wide")
st.title("\ud83d\udcd8 Audiobook Text-to-Speech with ElevenLabs")

# Sidebar options
st.sidebar.title("Settings")
selected_voice_name = st.sidebar.selectbox("\ud83c\udfa7 Choose a Voice", list(ELEVENLABS_VOICES.keys()))
voice_id = ELEVENLABS_VOICES[selected_voice_name]

# Upload or input section
upload_option = st.radio("Select input method:", ["\ud83d\udcdd Paste text", "\ud83d\udcc2 Upload file (.txt, .docx)"])

text = ""
uploaded_file = None

if upload_option == "\ud83d\udcdd Paste text":
    text = st.text_area("Paste your chapter or paragraph:", height=300)
elif upload_option == "\ud83d\udcc2 Upload file (.txt, .docx)":
    uploaded_file = st.file_uploader("Upload a .txt or .docx file", type=["txt", "docx"])
    if uploaded_file is not None:
        if uploaded_file.type == "text/plain":
            text = uploaded_file.read().decode("utf-8")
        elif uploaded_file.type == "application/vnd.openxmlformats-officedocument.wordprocessingml.document":
            doc = docx.Document(uploaded_file)
            text = "\n".join([para.text for para in doc.paragraphs])
        st.text_area("File Preview", text, height=300)

# Generate and play audio
if st.button("\u25b6\ufe0f Generate & Play Audio"):
    if not text.strip():
        st.warning("Please enter or upload text.")
    elif ELEVENLABS_API_KEY == "your-api-key-here":
        st.error("Please update the API key in the code.")
    else:
        with st.spinner("Generating audio from ElevenLabs..."):
            try:
                url = f"https://api.elevenlabs.io/v1/text-to-speech/{voice_id}"
                headers = {
                    "xi-api-key": ELEVENLABS_API_KEY,
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
                response = requests.post(url, json=payload, headers=headers)

                if response.status_code == 200:
                    audio_bytes = io.BytesIO(response.content)
                    st.audio(audio_bytes, format="audio/mp3")

                    st.success("\u2705 Audio generated!")
                    st.download_button(
                        label="\u2b07\ufe0f Download MP3",
                        data=audio_bytes,
                        file_name="audiobook.mp3",
                        mime="audio/mpeg"
                    )
                else:
                    st.error(f"\u26a0\ufe0f Error: {response.status_code} - {response.text}")
            except Exception as e:
                st.error(f"Unexpected error: {e}")
