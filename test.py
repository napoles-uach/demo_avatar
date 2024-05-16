import streamlit as st
import speech_recognition as sr
from gtts import gTTS
from io import BytesIO
import base64
from streamlit_avatar import avatar

st.title("Real-time Speech-to-Text and Text-to-Speech")

# Create an empty placeholder for the transcribed text
text_placeholder = st.empty()

# Initialize recognizer
recognizer = sr.Recognizer()

def recognize_speech():
    """Listen and transcribe speech using the microphone."""
    with sr.Microphone() as source:
        st.write("Adjusting for ambient noise...")
        recognizer.adjust_for_ambient_noise(source)
        st.write("Listening...")
        audio = recognizer.listen(source)

    try:
        text = recognizer.recognize_google(audio)
        return text
    except sr.RequestError:
        return "API unavailable"
    except sr.UnknownValueError:
        return "Unable to recognize speech"

def text_to_speech(text):
    """Convert text to speech using gTTS."""
    tts = gTTS(text)
    audio_buffer = BytesIO()
    tts.write_to_fp(audio_buffer)
    audio_buffer.seek(0)
    return audio_buffer

def main():
    st.write("Click the button and speak. The recognized text will be displayed below.")

    if st.button("Speak"):
        with st.spinner('Listening...'):
            text = recognize_speech()

        if text not in ["API unavailable", "Unable to recognize speech"]:
            text_placeholder.write(f"You said: {text}")

            # Convert text to speech
            audio_buffer = text_to_speech(text)
            audio_base64 = base64.b64encode(audio_buffer.read()).decode()
            st.audio(f"data:audio/wav;base64,{audio_base64}", format="audio/wav")

            # Use the avatar component to display the text
            avatar(text)
        else:
            text_placeholder.write(f"Error: {text}")

if __name__ == "__main__":
    main()


