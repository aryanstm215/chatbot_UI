import streamlit as st
from langchain.chains import LLMChain
from langchain.llms import HuggingFaceHub
from langchain.prompts import PromptTemplate
import os
from dotenv import load_dotenv
import time
from gtts import gTTS
import base64

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
