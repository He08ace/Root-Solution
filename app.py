import streamlit as st
import requests
import tempfile
import uuid

# App Title
st.title("📖 Audiobook Reader with ElevenLabs")

# Sidebar: API Key and Voice Selection
st.sidebar.header("Settings")

# Load API key from Streamlit secrets
api_key = st.secrets.get("ELEVENLABS_API_KEY", "")

if not api_key:
    st.sidebar.error("⚠️ Add your ElevenLabs API key to Streamlit secrets!")
    st.stop()

# Voice Options
voice_options = {
    "Rachel": "21m00Tcm4TlvDq8ikWAM",
    "Domi": "AZnzlk1XvdvUeBnXmlld",
    "Bella": "EXAVITQu4vr4xnSDxMaL",
    "Antoni": "ErXwobaYiN019PkySvjV",
    "Elli": "MF3mGyEYCl7XYWbV9V6O",
    "Josh": "TxGEqnHWrfWFTfGW9XjX"
}

# Voice Selection
voice_name = st.sidebar.selectbox("Choose a Voice", list(voice_options.keys()))
voice_id = voice_options[voice_name]

# Upload file or enter text
uploaded_file = st.file_uploader("📁 Upload a .txt file (or enter text below)", type=["txt"])

raw_text = ""
if uploaded_file:
    raw_text = uploaded_file.read().decode("utf-8")
else:
    raw_text = st.text_area("✍️ Or type/paste your content here", height=300)

# Split by chapters if present
chapters = []
if "# Chapter" in raw_text:
    raw_chunks = raw_text.split("# Chapter")
    for i, chunk in enumerate(raw_chunks):
        cleaned = chunk.strip()
        if cleaned:
            chapters.append(f"Chapter {i+1}" if i > 0 else "Introduction")
            chapters[i-1 if i > 0 else 0] = cleaned
    chapter_selection = st.selectbox("📘 Choose a Chapter", list(chapters))
    selected_text = chapters[list(chapters).index(chapter_selection)]
else:
    selected_text = raw_text

# Generate and Play
if st.button("▶️ Play with ElevenLabs Voice"):
    if not selected_text:
        st.warning("⚠️ Please enter or upload text.")
    else:
        with st.spinner("🎙️ Generating audio..."):
            try:
                url = f"https://api.elevenlabs.io/v1/text-to-speech/{voice_id}"

                headers = {
                    "xi-api-key": api_key,
                    "Content-Type": "application/json"
                }

                payload = {
                    "text": selected_text,
                    "model_id": "eleven_monolingual_v1",
                    "voice_settings": {
                        "stability": 0.5,
                        "similarity_boost": 0.75
                    }
                }

                response = requests.post(url, json=payload, headers=headers)

                if response.status_code == 200:
                    audio_bytes = response.content
                    st.audio(audio_bytes, format="audio/mp3")

                    # Save to file for download
                    tmp_filename = f"{uuid.uuid4().hex}.mp3"
                    with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as tmp_file:
                        tmp_file.write(audio_bytes)
                        tmp_path = tmp_file.name

                    st.download_button("⬇️ Download Audio", data=audio_bytes, file_name=tmp_filename, mime="audio/mpeg")
                else:
                    st.error(f"⚠️ Failed: {response.status_code} - {response.text}")
            except Exception as e:
                st.error(f"❌ Error: {e}")
