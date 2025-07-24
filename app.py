import streamlit as st
import requests
import os
from pydub import AudioSegment
from io import BytesIO
from docx import Document

# 🔒 Get ElevenLabs API Key securely from Streamlit secrets
ELEVENLABS_API_KEY = st.secrets["ELEVENLABS_API_KEY"]

# Voice options from ElevenLabs (name: voice_id)
VOICE_OPTIONS = {
    "Rachel": "21m00Tcm4TlvDq8ikWAM",
    "Domi": "AZnzlk1XvdvUeBnXmlld",
    "Bella": "EXAVITQu4vr4xnSDxMaL",
    "Antoni": "ErXwobaYiN019PkySvjV",
    "Elli": "MF3mGyEYCl7XYWbV9V6O"
}

# App title and description
st.set_page_config(page_title="Audiobook TTS Reader", layout="centered")
st.title("📖 Audiobook TTS Reader")
st.markdown("Convert your text or documents into lifelike audio using ElevenLabs text-to-speech.")

# Sidebar: Voice selection
with st.sidebar:
    st.header("🎙 Voice Options")
    selected_voice_name = st.selectbox("Choose a voice", list(VOICE_OPTIONS.keys()))
    selected_voice_id = VOICE_OPTIONS[selected_voice_name]

# File uploader and manual input
uploaded_file = st.file_uploader("📄 Upload a .txt or .docx file", type=["txt", "docx"])
text_input = st.text_area("✏️ Or paste your own text here", height=200)

# Function to read uploaded file
def read_text(file):
    if file.name.endswith(".txt"):
        return file.read().decode("utf-8")
    elif file.name.endswith(".docx"):
        doc = Document(file)
        return "\n".join([para.text for para in doc.paragraphs])
    return ""

# Get text from file or manual input
text = ""
if uploaded_file:
    text = read_text(uploaded_file)
elif text_input:
    text = text_input

# Function to generate speech with ElevenLabs
def generate_audio(text, voice_id):
    url = f"https://api.elevenlabs.io/v1/text-to-speech/{voice_id}"
    headers = {
        "xi-api-key": ELEVENLABS_API_KEY,
        "Content-Type": "application/json"
    }
    payload = {
        "text": text,
        "voice_settings": {
            "stability": 0.5,
            "similarity_boost": 0.75
        }
    }
    response = requests.post(url, headers=headers, json=payload)
    if response.status_code == 200:
        return BytesIO(response.content)
    else:
        st.error(f"⚠️ Failed to generate audio: {response.status_code} - {response.text}")
        return None

# Play and download button
if st.button("▶️ Play with ElevenLabs Voice"):
    if text:
        with st.spinner("🎧 Generating audio..."):
            audio_data = generate_audio(text, selected_voice_id)
            if audio_data:
                st.audio(audio_data, format="audio/mp3")
                st.download_button("⬇️ Download Audio", audio_data, file_name="audiobook.mp3")
    else:
        st.warning("Please upload a file or enter some text above.")
