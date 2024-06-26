import streamlit as st
from transformers import MBartForConditionalGeneration, MBart50Tokenizer
import torch
from dotenv import load_dotenv
import os

load_dotenv()
HUGGINGFACE_API_KEY = os.getenv("HUGGINGFACE_API_KEY")

# Function to load model and tokenizer with API key
def load_model_and_tokenizer(model_name, api_key):
    model = MBartForConditionalGeneration.from_pretrained(model_name, use_auth_token=api_key)
    tokenizer = MBart50Tokenizer.from_pretrained(model_name, use_auth_token=api_key)
    return model, tokenizer

# Load the MBart model and tokenizer
model_name = "facebook/mbart-large-50-many-to-many-mmt"
model, tokenizer = load_model_and_tokenizer(model_name, HUGGINGFACE_API_KEY)

# Function to generate translations
def translate_text(input_text, target_language):
    tokenizer.src_lang = "en_XX"  # Set source language to English
    inputs = tokenizer(input_text, return_tensors="pt")
    forced_bos_token_id = tokenizer.lang_code_to_id[target_language]
    outputs = model.generate(**inputs, forced_bos_token_id=forced_bos_token_id, max_length=512, num_beams=5, num_return_sequences=1, temperature=0.5)
    translation = tokenizer.decode(outputs[0], skip_special_tokens=True)
    return translation

# Streamlit UI setup
st.title("Multilingual Chatbot for Translation")

# Initialize chat history
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# Define columns for bot and user
col1, col2 = st.columns(2)

# Placeholder for user input
user_input_placeholder = st.empty()

# Display the chat history
for chat in st.session_state.chat_history:
    if chat["is_user"]:
        with col2:
            st.write(f"You: {chat['message']}")
    else:
        with col1:
            st.write(f"Bot: {chat['message']}")

# Target language selection
with col1:
    target_language = st.selectbox("Select target language:", ["fr_XX", "de_DE", "es_XX", "it_IT", "hi_IN"], key="target_language")

# Bot's turn to ask a question
bot_prompt = "Please provide a text to translate:"
with col1:
    st.write(f"Bot: {bot_prompt}")

# Unique key for user input
user_input_key = f"user_input_{len(st.session_state.chat_history)}"

# User input
user_input = user_input_placeholder.text_input("You:", key=user_input_key)

# Process the user input
if user_input:
    # Append user message to chat history
    st.session_state.chat_history.append({"message": user_input, "is_user": True})

    # Translate the text
    translation = translate_text(user_input, target_language)

    # Append bot response to chat history
    st.session_state.chat_history.append({"message": translation, "is_user": False})

    # Clear the input field by reinitializing the placeholder with a new unique key
    user_input_key = f"user_input_{len(st.session_state.chat_history)}"
    user_input_placeholder.text_input("You:", value="", key=user_input_key)

# Ensure the conversation continues to flow naturally by prompting again after user input
if user_input:
    st.experimental_rerun()
