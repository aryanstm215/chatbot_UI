import requests
import json
import os
import fitz  # PyMuPDF
from googletrans import Translator

# Define the languages you want to translate to
languages = ['es', 'fr', 'de', 'zh-cn', 'ja', 'hi']  

# Instructions for OCR processing
instructions = {
    'parts': [
        {
            'file': 'scanned'
        }
    ],
    'actions': [
        {
            'type': 'ocr',
            'language': 'english'
        }
    ]
}

# Make the API request
response = requests.request(
    'POST',
    'https://api.pspdfkit.com/build',
    headers={
        'Authorization': 'Bearer pdf_live_waa9XMBcfYXbXMw691daAiRkTueALiGnvTasQFXKRyl'
    },
    files={
        'scanned': open('Aryan_Resume.pdf', 'rb')
    },
    data={
        'instructions': json.dumps(instructions)
    },
    stream=True
)

# Check if the request was successful
if response.ok:
    # Save the response content to a file
    with open('processed_file.pdf', 'wb') as f:
        for chunk in response.iter_content(chunk_size=8096):
            if chunk:
                f.write(chunk)

    # Now you need to extract the text from the processed PDF file
    document = fitz.open('processed_file.pdf')

    # Extract text from each page
    extracted_text = ""
    for page_num in range(len(document)):
        page = document.load_page(page_num)
        extracted_text += page.get_text()

    # Print the extracted text
    print("Extracted Text:")
    print(extracted_text)

    # Initialize the translator
    translator = Translator()

    # Translate the extracted text into multiple languages
    translations = {}
    for lang in languages:
        translated = translator.translate(extracted_text, dest=lang)
        translations[lang] = translated.text

    # Print translations
    for lang, text in translations.items():
        print(f"\nTranslated Text ({lang}):")
        print("==========================================")
        print(text)

    # Optionally, clean up the temporary file
    os.remove('processed_file.pdf')
else:
    print("Error:", response.text)