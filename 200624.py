import streamlit as st
import requests
import json
import os
import fitz  # PyMuPDF
from googletrans import Translator
from langchain.chains import LLMChain
from langchain.llms import HuggingFaceHub
from langchain.prompts import PromptTemplate
import time
from gtts import gTTS
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Initialize session state
if 'chat_history' not in st.session_state:
    st.session_state.chat_history = []

# Function to perform text translation
def Translate_Text(user_text, target_language):
    api_token = os.getenv('HUGGINGFACEHUB_API_TOKEN')
    if not api_token:
        raise ValueError("Hugging Face API token not found in environment variables.")

    prompt_template = """
    Translate the following text from English to {target_language}:

    English: {user_text}
    Translation:
    """

    prompt = PromptTemplate.from_template(prompt_template)
    chain = LLMChain(
        llm=HuggingFaceHub(repo_id='mistralai/Mistral-7B-Instruct-v0.2', model_kwargs={'temperature': 0.5, 'max_new_tokens': 50}, huggingfacehub_api_token=api_token),
        prompt=prompt
    )
    result = chain.run(user_text=user_text, target_language=target_language)

    # Parse the result to extract only the translation
    translation = result.split("Translation:")[1].strip().split('\n')[0]
    
    return translation

def generate_audio(text, lang):
    # Map target language to gTTS supported language code
    lang_code_map = {
        "English": "en",
        "Spanish": "es",
        "French": "fr",
        "German": "de",
        "Italian": "it",
        "Chinese": "zh",
        "Japanese": "ja",
        "Russian": "ru",
        "Hindi": "hi",
        "Malayalam": "ml"
    }
    lang_code = lang_code_map.get(lang, "en")  # Default to English if the language is not found

    tts = gTTS(text=text, lang=lang_code)
    tts.save("output.mp3")
    with open("output.mp3", "rb") as audio_file:
        audio_bytes = audio_file.read()
    return audio_bytes

def display_message(chat_message):
    role = chat_message["role"]
    content = chat_message["content"]

    if role == "user":
        st.markdown(f"<div style='text-align: right; margin-bottom: 20px;'><b>🙂 You:</b> {content}</div>", unsafe_allow_html=True)
    elif role == "loading":
        st.image("https://miro.medium.com/v2/resize:fit:720/format:webp/0*NfFRP_WMxD-XT14o.gif", width=300)
    else:
        st.markdown(f"<div style='text-align: left; margin-top: 20px; margin-bottom: 20px;'><b style='font-size:24px;'>🤖:</b> {content}</div>", unsafe_allow_html=True)
        if 'audio' in chat_message:
            audio_bytes = chat_message['audio']
            st.audio(audio_bytes, format="audio/mp3")

# Streamlit front-end
st.title("Text Translation Chatbot")

# Display greeting message only if chat history is empty
if not st.session_state.chat_history:
    st.session_state.chat_history.append({"role": "bot", "content": "Hello! Welcome to the text translation chatbot. Please enter the text you want to translate and select the target language."})

# Display chat history
for chat_message in st.session_state.chat_history[:-1]:
    display_message(chat_message)

# Input from user
with st.form("user_input_form"):
    user_input = st.text_input("You:")
    target_language = st.selectbox("Select target language", ["English", "Spanish", "French", "German", "Italian", "Chinese", "Japanese", "Russian", "Hindi", "Malayalam"])
    submit_button = st.form_submit_button("Submit")

# If user submits the form
if submit_button and user_input:
    st.session_state.chat_history.append({"role": "user", "content": user_input})
    st.session_state.chat_history.append({"role": "loading", "content": "loading"})
    # Rerun to display loading state
    st.experimental_rerun()

# If loading state is in session history
if st.session_state.chat_history and st.session_state.chat_history[-1]["role"] == "loading":
    time.sleep(2)  # Simulate loading time
    translation = Translate_Text(st.session_state.chat_history[-2]["content"], target_language)
    st.session_state.chat_history.pop()  # Remove loading message
    audio_bytes = generate_audio(translation, target_language)
    st.session_state.chat_history.append({"role": "bot", "content": translation, "audio": audio_bytes})
    # Rerun to display translated text and audio
    st.experimental_rerun()

# Display only the last message to avoid repetition
if st.session_state.chat_history:
    display_message(st.session_state.chat_history[-1])

# OCR and Translation Section
st.header("OCR and Translation")

# File uploader for OCR
uploaded_file = st.file_uploader("Upload a PDF file", type="pdf")

if uploaded_file is not None:
    target_language = st.selectbox("Select target language for OCR", ["English", "Spanish", "French", "German", "Italian", "Chinese", "Japanese", "Russian", "Hindi", "Malayalam"])
    ocr_button = st.button("Perform OCR and Translate")

    if ocr_button:
        with open("uploaded_file.pdf", "wb") as f:
            f.write(uploaded_file.getbuffer())

        # Perform OCR using PSPDFKit API
        instructions = {
            'parts': [{'file': 'scanned'}],
            'actions': [{'type': 'ocr', 'language': 'english'}]  # Adjust language if PSPDFKit supports other languages
        }

        response = requests.request(
            'POST',
            'https://api.pspdfkit.com/build',
            headers={'Authorization': 'Bearer pdf_live_Dx9q0OnYtkjlTDT3LYUqLqIR9UDQCQPTHsodJw5uydx'},
            files={'scanned': open('uploaded_file.pdf', 'rb')},
            data={'instructions': json.dumps(instructions)},
            stream=True
        )

        if response.ok:
            with open('processed_file.pdf', 'wb') as f:
                for chunk in response.iter_content(chunk_size=8096):
                    if chunk:
                        f.write(chunk)

            document = fitz.open('processed_file.pdf')
            extracted_text = ""
            for page_num in range(len(document)):
                page = document.load_page(page_num)
                extracted_text += page.get_text()

            st.text_area("Extracted Text", value=extracted_text, height=300)

            # Mapping target languages to Google Translate language codes
            lang_code_map = {
                "English": "en",
                "Spanish": "es",
                "French": "fr",
                "German": "de",
                "Italian": "it",
                "Chinese": "zh-cn",
                "Japanese": "ja",
                "Russian": "ru",
                "Hindi": "hi",
                "Malayalam": "ml"
            }

            target_lang_code = lang_code_map.get(target_language, "en")  # Default to English if not found
            translator = Translator()
            translated = translator.translate(extracted_text, dest=target_lang_code)  # Adjust target language code as needed
            translation = translated.text

            st.markdown(f"### Translated Text ({target_language})")
            st.text_area(f"Translation ({target_language})", value=translation, height=150)

            os.remove('processed_file.pdf')
        else:
            st.error("Error processing the document: " + response.text)
