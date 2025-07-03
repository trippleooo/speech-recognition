
import streamlit as st
import speech_recognition as sr
import os

# Available languages
LANGUAGES = {
    "English (US)": "en-US",
    "French": "fr-FR",
    "Swahili": "sw-KE",
    "Spanish": "es-ES",
    "German": "de-DE"
}

# Available APIs
APIS = ["Google", "Sphinx"]

# Function to transcribe speech
def transcribe_speech(api_choice, language):
    recognizer = sr.Recognizer()
    try:
        with sr.Microphone() as source:
            st.info("Speak now...")
            audio = recognizer.listen(source, timeout=5, phrase_time_limit=10)
            st.info("Transcribing...")

            if api_choice == "Google":
                return recognizer.recognize_google(audio, language=language)
            elif api_choice == "Sphinx":
                return recognizer.recognize_sphinx(audio, language=language)
            else:
                return "Unsupported API selected."

    except sr.WaitTimeoutError:
        return "No speech detected."
    except sr.UnknownValueError:
        return "Could not understand audio."
    except sr.RequestError as e:
        return f"API Error: {e}"
    except Exception as e:
        return f"Error: {e}"

# Function to save text
def save_transcription(text):
    if text:
        with open("transcription.txt", "a") as f:
            f.write(text + "\n")
        st.success("Transcription saved.")

# Main app logic
def main():
    st.set_page_config(page_title="Speech Recognition App", layout="centered")
    st.title("Speech Recognition App")
    st.markdown("Speak into the microphone and convert your speech to text.")

    language = st.selectbox("Select Language", list(LANGUAGES.keys()))
    lang_code = LANGUAGES[language]

    api_choice = st.radio("Choose Speech Recognition API", APIS)

    if st.button("Start Recording"):
        text = transcribe_speech(api_choice, lang_code)
        st.write("**Transcription:**", text)

        if text and "Sorry" not in text:
            if st.checkbox("Save this transcription?"):
                save_transcription(text)

    if os.path.exists("transcription.txt"):
        with open("transcription.txt", "r") as f:
            st.text_area("📄 Saved Transcriptions", f.read(), height=200)

if __name__ == "__main__":
    main()
