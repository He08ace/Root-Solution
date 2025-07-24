import streamlit as st
import requests
import io
from docx import Document
from pydub import AudioSegment
from pydub.playback import play
import base64

# --- Config ---
st.set_page_config(page_title="📚 Audiobook TTS Reader", layout="centered")
st.title("🎧 Audiobook Text-to-Speech Reader")

# --- ElevenLabs Setup ---
API_KEY = st.secrets["ELEVENLABS_API_KEY"]
VOICE_OPTIONS = {
    "Rachel (female)": "21m00Tcm4TlvDq8ikWAM",
    "Domi (female)": "AZnzlk1XvdvUeBnXmlld",
    "Bella (female)": "EXAVITQu4vr4xnSDxMaL",
    "Antoni (male)": "ErXwobaYiN019PkySvjV",
    "Elli (child)": "MF3mGyEYCl7XYWbV9V6O"
}
voice_choice = st.selectbox("🎙️ Choose a Voice", list(VOICE_OPTIONS.keys()))
voice_id = VOICE_OPTIONS[voice_choice]

# --- File Upload / Text Input ---
uploaded_file = st.file_uploader("📁 Upload a .txt or .docx file", type=["txt", "docx"])
raw_text = ""

if uploaded_file:
    file_type = uploaded_file.name.split(".")[-1]
    if file_type == "txt":
        raw_text = uploaded_file.read().decode("utf-8")
    elif file_type == "docx":
        doc = Document(uploaded_file)
        raw_text = "\n".join([para.text for para in doc.paragraphs])
else:
    raw_text = st.text_area("✍️ Or type/paste your content here", height=300)

# --- TTS Function ---
def get_audio_from_elevenlabs(text, voice_id):
    url = f"https://api.elevenlabs.io/v1/text-to-speech/{voice_id}"
    headers = {
        "xi-api-key": API_KEY,
        "Content-Type": "application/json"
    }
    payload = {
        "text": text,
        "model_id": "eleven_monolingual_v1",
        "voice_settings": {"stability": 0.5, "similarity_boost": 0.75}
    }
    response = requests.post(url, headers=headers, json=payload)
    
    if response.status_code == 200:
        return response.content
    else:
        st.error(f"⚠️ Failed to generate audio: {response.status_code} - {response.text}")
        return None

# --- Generate & Play Audio ---
if st.button("▶️ Play with ElevenLabs Voice"):
    if not raw_text:
        st.warning("⚠️ Please upload a file or enter text.")
    else:
        with st.spinner("🌀 Generating audio..."):
            audio_bytes = get_audio_from_elevenlabs(raw_text, voice_id)
            if audio_bytes:
                st.audio(audio_bytes, format="audio/mp3")
