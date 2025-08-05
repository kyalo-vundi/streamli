import streamlit as st
import speech_recognition as sr
import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
import string

# Download required NLTK data
nltk.download('punkt')
nltk.download('stopwords')
nltk.download('wordnet')

# Initialize speech recognizer
recognizer = sr.Recognizer()

# Preprocess text data (assumes a conversational dataset)
def preprocess_text(text):
    lemmatizer = WordNetLemmatizer()
    stop_words = set(stopwords.words('english'))
    tokens = word_tokenize(text.lower())
    tokens = [lemmatizer.lemmatize(token) for token in tokens if token not in string.punctuation and token not in stop_words]
    return tokens

# Simple chatbot response generation (rule-based)
def chatbot_response(user_input):
    processed_input = preprocess_text(user_input)
    # Example rule-based responses (replace with your dataset logic)
    greetings = ['hello', 'hi', 'hey']
    if any(token in processed_input for token in greetings):
        return "Hi! How can I help you today?"
    elif 'weather' in processed_input:
        return "I’m not connected to a weather API, but I can chat about sunny vibes!"
    elif 'name' in processed_input:
        return "I’m Grok, your friendly AI assistant!"
    else:
        return "Hmm, interesting! Can you tell me more?"

# Function to transcribe speech to text
def transcribe_speech():
    with sr.Microphone() as source:
        st.write("Listening... Speak clearly!")
        recognizer.adjust_for_ambient_noise(source)
        try:
            audio = recognizer.listen(source, timeout=5)
            text = recognizer.recognize_google(audio)
            st.write(f"Transcribed: {text}")
            return text
        except sr.WaitTimeoutError:
            return "No speech detected. Please try again."
        except sr.UnknownValueError:
            return "Sorry, I couldn’t understand the audio."
        except sr.RequestError:
            return "Speech recognition service is unavailable."

# Streamlit app
def main():
    st.title("Speech-Enabled Chatbot")
    st.write("Type your message or click 'Speak' to use voice input.")

    # Text input
    user_text = st.text_input("Enter your message:")
    if user_text:
        response = chatbot_response(user_text)
        st.write(f"*Chatbot:* {response}")

    # Speech input
    if st.button("Speak"):
        with st.spinner("Processing speech..."):
            transcribed_text = transcribe_speech()
            st.write(f"*You said:* {transcribed_text}")
            if not transcribed_text.startswith("Sorry") and not transcribed_text.startswith("No speech"):
                response = chatbot_response(transcribed_text)
                st.write(f"*Chatbot:* {response}")

if __name__ == "_main_":
    main()