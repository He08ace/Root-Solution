import streamlit as st
import requests
import base64

# App Title
st.title("📖 Audiobook Reader with ElevenLabs")

# Sidebar: API Key and Voice Selection
st.sidebar.header("Settings")

# API Key input via Streamlit secrets
api_key = st.secrets.get("ELEVENLABS_API_KEY", "")

if not api_key:
    st.sidebar.error("⚠️ Add your ElevenLabs API key to Streamlit secrets!")
    st.stop()

# List of available ElevenLabs voices
voice_options = {
    "Rachel": "21m00Tcm4TlvDq8ikWAM",
    "Domi": "AZnzlk1XvdvUeBnXmlld",
    "Bella": "EXAVITQu4vr4xnSDxMaL",
    "Antoni": "ErXwobaYiN019PkySvjV",
    "Elli": "MF3mGyEYCl7XYWbV9V6O",
    "Josh": "TxGEqnHWrfWFTfGW9XjX",
    "Arnold (Custom)": "VR6AewLTigWG4xSOukaG",  # Optional
}

voice_name = st.sidebar.selectbox("Select Voice", list(voice_options.keys()))
voice_id = voice_options[voice_name]

# Main text input
st.subheader("📚 Paste Your Audiobook Chapter")
text_input = st.text_area("Enter the text you want to hear:", height=300)

if st.button("▶️ Play with ElevenLabs Voice"):
    if not text
