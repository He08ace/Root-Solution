import streamlit as st
import requests
import base64
from docx import Document
import os

# Get ElevenLabs API key from Streamlit secrets
API_KEY = st.secrets["elevenlabs"]["api_key"]

# ElevenLabs endpoint
TTS_ENDPOINT = "https://api.elevenlabs.io/v1/text-to-speech"

# Set page config
st.set_page_config(page_title="📖 Audiobook Reader", layout="centered")

st.title("📖 Text-to-Speech Audiobook Reader")

# Sidebar settings
st.sidebar.title("🔧 Settings")

# Select voice from dropdown (update as needed)
voice_options = {
    "Rachel": "21m00Tcm4TlvDq8ikWAM", 
    "Domi": "AZnzlk1XvdvUeBnXmlld", 
    "Bella": "EXAVITQu4vr4xnSDxMaL"
}
voice_name = st.sidebar.selectbox("Choose a voice:", list(voice_options.keys()))
voice_id = voice_options[voice_name]

# Upload or paste text
uploaded_file = st.file_uploader("📄 Upload a .txt or .docx file", type=["txt", "docx"])
text_input = st.text_area("📝 Or paste your text here", height=200)

def read_uploaded_file(file):
    if file.name.endswith(".txt"):
        return file.read().decode("utf-8")
    elif file.name.endswith(".docx"):
        doc = Document(file)
        return "\n".join([para.text for para in doc.paragraphs])
    else:
        return ""

def generate_audio(text, voice_id):
    headers = {
        "xi-api-key": API_KEY,
        "Content-Type": "application/json"
    }

    data = {
        "text": text,
        "voice_settings": {
            "stability": 0.75,
            "similarity_boost": 0.75
        }
    }

    url = f"{TTS_ENDPOINT}/{voice_id}/stream"
    response = requests.post(url, headers=headers, json=data)

    if response.status_code == 200:
        return response.content
    else:
        st.error(f"⚠️ Failed to generate audio: {response.status_code} - {response.text}")
        return None

# Main logic
if uploaded_file:
    text = read_uploaded_file
