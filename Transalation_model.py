import streamlit as st
from transformers import T5ForConditionalGeneration, T5Tokenizer
import torch
from dotenv import load_dotenv
import os

load_dotenv()
HUGGINGFACE_API_KEY = os.getenv("HUGGINGFACE_API_KEY")

# Function to load model and tokenizer with API key
def load_model_and_tokenizer(model_name, api_key):
    model = T5ForConditionalGeneration.from_pretrained(model_name, use_auth_token=api_key)
    tokenizer = T5Tokenizer.from_pretrained(model_name, use_auth_token=api_key)
    return model, tokenizer

# Load the T5 model and tokenizer
model_name = "t5-base"
model, tokenizer = load_model_and_tokenizer(model_name, HUGGINGFACE_API_KEY)

# Function to generate translations
def translate_text(input_text, target_language):
    prompt = f"translate English to {target_language}: {input_text}"
    inputs = tokenizer.encode(prompt, return_tensors="pt")
    outputs = model.generate(inputs, max_length=512, num_beams=5, num_return_sequences=1, temperature=1.5)
    translation = tokenizer.decode(outputs[0], skip_special_tokens=True)
    return translation

# Streamlit UI setup
st.title("Multilingual Chatbot for Translation")

# Initialize chat history
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# Define columns for bot and user
col1, col2 = st.columns(2)

# Target language selection
target_language = st.selectbox("Select target language:", ["French", "German", "Spanish", "Italian"], key="target_language")

# Placeholder for user input
user_input_placeholder = st.empty()

# Unique key for user input
user_input_key = f"user_input_{len(st.session_state.chat_history)}"

# User input
user_input = user_input_placeholder.text_input("You:", key=user_input_key)

# Bot's turn to ask a question
if user_input:
    # Append user message to chat history
    st.session_state.chat_history.append({"message": user_input, "is_user": True})

    # Translate the text
    translation = translate_text(user_input, target_language.lower())

    # Append bot response to chat history
    st.session_state.chat_history.append({"message": translation, "is_user": False})

    # Clear the input field by reinitializing the placeholder with a new unique key
    user_input_key = f"user_input_{len(st.session_state.chat_history)}"
    user_input_placeholder.text_input("You:", value="", key=user_input_key)

# Display chat messages from history on app rerun
for i, chat in enumerate(st.session_state.chat_history):
    if chat["is_user"]:
        with col2:
            st.write(f"You: {chat['message']}")
    else:
        with col1:
            st.write(f"Bot: {chat['message']}")

# Prompt bot to ask a question
with col1:
    bot_prompt = "Please provide a text to translate:"
    st.write(f"Bot: {bot_prompt}")
