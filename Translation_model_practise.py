import streamlit as st
from langchain.chains import LLMChain
from langchain.llms import HuggingFaceHub
from langchain.prompts import PromptTemplate
import os
from dotenv import load_dotenv

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
    
    return f"**Input Text:** `{user_text}`\n**Target Language:** `{target_language}`\n**Translation:** `{translation}`"

def display_message(chat_message):
    role = chat_message["role"]
    content = chat_message["content"]

    if role == "user":
        st.markdown(f"<div style='text-align: right; margin-bottom: 20px;'><b>You:</b> {content}</div>", unsafe_allow_html=True)
    else:
        st.markdown(f"<div style='text-align: left; margin-top: 20px;'><b>🤖:</b> {content}</div>", unsafe_allow_html=True)

# Streamlit front-end
st.title("Text Translation Chatbot")

# Display greeting message only if chat history is empty
if not st.session_state.chat_history:
    st.session_state.chat_history.append({"role": "bot", "content": "Hello! Welcome to the text translation chatbot. Please enter the text you want to translate and select the target language."})

# Display chat history
for chat_message in st.session_state.chat_history:
    display_message(chat_message)

# Input from user
with st.form("user_input_form"):
    user_input = st.text_input("You:")
    target_language = st.selectbox("Select target language", ["English", "Spanish", "French", "German", "Italian", "Chinese", "Japanese", "Russian","hindi","Malayalam"])
    submit_button = st.form_submit_button("Submit")

# If user submits the form
if submit_button:
    st.session_state.chat_history.append({"role": "user", "content": user_input})

    if user_input:
        translated_text = Translate_Text(user_input, target_language)
        st.session_state.chat_history.append({"role": "bot", "content": translated_text})

    # Reset form inputs
    user_input = ""
    target_language = "English"

    # Display updated chat history
    for chat_message in st.session_state.chat_history:
        display_message(chat_message)
