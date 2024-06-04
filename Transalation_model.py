import streamlit as st
import torch
from transformers import T5Tokenizer
from transformers.models.t5 import T5ForConditionalGeneration

# Load the T5 model and tokenizer
model = T5ForConditionalGeneration.from_pretrained("google-t5/t5-base")
tokenizer = T5Tokenizer.from_pretrained("google-t5/t5-base")

# Define the prompt template
prompt_template = """translate {input_text} to {target_lang}:"""

# Define the target languages and their codes
target_langs = {
    "English": "en",
    "Spanish": "es",
    "French": "fr",
    "German": "de",
    "Italian": "it",
    "Russian": "ru",
    "Japanese": "ja",
    "Chinese (Simplified)": "zh",
}

# Streamlit app
def app():
    st.set_page_config(page_title="Translation Chatbot", page_icon=":robot_face:")
    st.title("Translation Chatbot")

    # Initialize the chat history
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []

    # Get user input
    user_input = st.text_area("Enter your text to translate:", height=200)
    target_lang = st.selectbox("Select the target language:", list(target_langs.keys()))

    # Translate the input text
    if user_input and st.button("Translate"):
        prompt = prompt_template.format(input_text=user_input, target_lang=target_langs[target_lang])
        input_ids = tokenizer.encode(prompt, return_tensors="pt")
        output_ids = model.generate(input_ids, max_length=200, num_beams=5, early_stopping=True)
        translation = tokenizer.decode(output_ids[0], skip_special_tokens=True)

        # Add the conversation to the chat history
        st.session_state.chat_history.append({"role": "user", "content": user_input})
        st.session_state.chat_history.append({"role": "assistant", "content": translation})

    # Display the chat history
    for chat in st.session_state.chat_history:
        if chat["role"] == "user":
            st.markdown("**User:**")
            st.write(chat["content"])
        else:
            st.markdown("**Assistant:**")
            st.write(chat["content"])
        st.markdown("---")

if __name__ == "__main__":
    app()