import streamlit as st
import requests

# App Title
st.title("📖 Audiobook Reader with ElevenLabs")

# Sidebar: API Key and Voice Selection
st.sidebar.header("Settings")

# Load API key from Streamlit secrets
api_key = st.secrets.get("ELEVENLABS_API_KEY", "")

if not api_key:
    st.sidebar.error("⚠️ Add your ElevenLabs API key to Streamlit secrets!")
    st.stop()

# Voice Options from ElevenLabs
voice_options = {
    "Rachel": "21m00Tcm4TlvDq8ikWAM",
    "Domi": "AZnzlk1XvdvUeBnXmlld",
    "Bella": "EXAVITQu4vr4xnSDxMaL",
    "Antoni": "ErXwobaYiN019PkySvjV",
    "Elli": "MF3mGyEYCl7XYWbV9V6O",
    "Josh": "TxGEqnHWrfWFTfGW9XjX"
}

# Voice selection
voice_name = st.sidebar.selectbox("Choose a Voice", list(voice_options.keys()))
voice_id = voice_options[voice_name]

# Main Input
st.subheader("📚 Enter Text Below")
text = st.text_area("Paste your audiobook content here", height=300)

# Play Button
if st.button("▶️ Play with ElevenLabs Voice"):
    if not text:
        st.warning("⚠️ Please enter some text first.")
    else:
        with st.spinner("🎙️ Generating audio..."):
            try:
                url = f"https://api.elevenlabs.io/v1/text-to-speech/{voice_id}"

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

                response = requests.post(url, json=payload, headers=headers)

                if response.status_code == 200:
                    st.audio(response.content, format="audio/mp3")
                else:
                    st.error(f"⚠️ Failed to generate audio: {response.status_code} - {response.text}")

            except Exception as e:
                st.error(f"❌ Unexpected error: {e}")
