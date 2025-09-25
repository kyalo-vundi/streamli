import streamlit as st
import speech_recognition as sr
from datetime import datetime

# Title
st.title("🎙️ Speech Recognition App")

st.sidebar.header("Settings")

api_choice = st.sidebar.selectbox(
    "Choose Speech Recognition API",
    ["Google", "Sphinx"]
)

language = st.sidebar.selectbox(
    "Select Language",
    ["en-US", "en-GB", "fr-FR", "es-ES", "de-DE", "sw-KE"]
)

pause_recognition = st.sidebar.checkbox("Pause Recognition")

recognizer = sr.Recognizer()


def transcribe_audio_file(file, api_choice, language):
    try:
        with sr.AudioFile(file) as source:
            st.info("Processing uploaded audio file...")
            audio = recognizer.record(source)

        if api_choice == "Google":
            return recognizer.recognize_google(audio, language=language)
        elif api_choice == "Sphinx":
            return recognizer.recognize_sphinx(audio, language=language)
        else:
            return "❌ API not supported."

    except sr.UnknownValueError:
        return "⚠️ Could not understand the audio."
    except sr.RequestError as e:
        return f"❌ API request error: {e}"
    except Exception as e:
        return f"❌ Error: {str(e)}"


# 🔥 Always use file upload (no microphone) in Streamlit Cloud
st.warning("🎤 Microphone is not supported on Streamlit Cloud. Please upload an audio file.")

if not pause_recognition:
    uploaded_file = st.file_uploader("Upload an audio file", type=["wav", "mp3"])
    if uploaded_file is not None:
        text = transcribe_audio_file(uploaded_file, api_choice, language)
        st.subheader("Transcription Result")
        st.write(text)

        if "❌" not in text and "⚠️" not in text:
            filename = f"transcription_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
            with open(filename, "w", encoding="utf-8") as f:
                f.write(text)
            with open(filename, "r", encoding="utf-8") as f:
                st.download_button("Download Transcription", f, file_name=filename)
else:
    st.warning("Recognition paused ⏸️. Uncheck pause to continue.")
