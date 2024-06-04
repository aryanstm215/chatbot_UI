import streamlit as st
from transformers import T5ForConditionalGeneration, T5Tokenizer
import torch

# Your Hugging Face API key
HUGGINGFACE_API_KEY = "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"

# Function to load model and tokenizer with API key
def load_model_and_tokenizer(model_name, api_key):
    headers = {"Authorization": f"Bearer {api_key}"}
    model = T5ForConditionalGeneration.from_pretrained(model_name, use_auth_token=api_key)
    tokenizer = T5Tokenizer.from_pretrained(model_name, use_auth_token=api_key)
    return model, tokenizer

# Load the T5 model and tokenizer
model_name = "google-t5/t5-base"
model, tokenizer = load_model_and_tokenizer(model_name, HUGGINGFACE_API_KEY)

# Function to generate translations
def translate_text(input_text, target_language):
    prompt = f"Translate English to {target_language}: {input_text}"
    inputs = tokenizer.encode(prompt, return_tensors="pt")
    outputs = model.generate(inputs, max_length=512, num_beams=5, num_return_sequences=3, temperature=1.5)
    translations = [tokenizer.decode(output, skip_special_tokens=True) for output in outputs]
    return translations

# Streamlit UI setup
st.title("Multilingual Chatbot for Translation")

# Initialize chat history
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# Define columns for bot and user
col1, col2 = st.columns(2)

# User input
with col2:
    user_input = st.text_input("You:", key="user_input")

# Bot's turn to ask a question
if user_input:
    # Append user message to chat history
    st.session_state.chat_history.append({"message": user_input, "is_user": True})

    # Get the target language from user input or selection
    target_language = st.selectbox("Select target language:", ["French", "German", "Spanish", "Italian"], key="target_language")

    # Translate the text
    translations = translate_text(user_input, target_language)

    # Append bot response to chat history
    for translation in translations:
        st.session_state.chat_history.append({"message": translation, "is_user": False})

# Display chat messages from history on app rerun
for chat in st.session_state.chat_history:
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
