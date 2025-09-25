import streamlit as st
import speech_recognition as sr
import os
from datetime import datetime

# Title
st.title("🎙️ Speech Recognition App (Improved)")

# Sidebar options
st.sidebar.header("Settings")

# API selection
api_choice = st.sidebar.selectbox(
    "Choose Speech Recognition API",
    ["Google", "Sphinx"]
)

# Language selection (ISO codes)
language = st.sidebar.selectbox(
    "Select Language",
    ["en-US", "en-GB", "fr-FR", "es-ES", "de-DE", "sw-KE"]
)

# Pause / Resume toggle
pause_recognition = st.sidebar.checkbox("Pause Recognition")

# Recognizer instance
recognizer = sr.Recognizer()
mic = sr.Microphone()

def transcribe_speech(api_choice, language):
    try:
        with mic as source:
            st.info("Adjusting for ambient noise... Please wait")
            recognizer.adjust_for_ambient_noise(source)
            st.success("Start speaking 🎤 (Recording...)")
            audio = recognizer.listen(source)

        if api_choice == "Google":
            return recognizer.recognize_google(audio, language=language)

        elif api_choice == "Sphinx":
            return recognizer.recognize_sphinx(audio, language=language)

        else:
            return "❌ API not supported."

    except sr.UnknownValueError:
        return "⚠️ Could not understand audio. Please try again."
    except sr.RequestError as e:
        return f"❌ Could not request results from {api_choice} API; {e}"
    except Exception as e:
        return f"❌ Error: {str(e)}"

# Run transcription
if not pause_recognition:
    if st.button("Start Transcription"):
        text = transcribe_speech(api_choice, language)
        st.subheader("Transcription Result")
        st.write(text)

        # Save to file
        if "❌" not in text and "⚠️" not in text:
            filename = f"transcription_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
            with open(filename, "w", encoding="utf-8") as f:
                f.write(text)
            with open(filename, "r", encoding="utf-8") as f:
                st.download_button("Download Transcription", f, file_name=filename)
else:
    st.warning("Recognition paused ⏸️. Uncheck pause to continue.")
