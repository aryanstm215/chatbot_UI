from gtts import gTTS

# Your text to convert to speech
text = "my name is Aaaryan , i am currently working as a Machine learning engineer in Chipmonk technology."

# Select language (default is 'en' for English)
language = 'en'

# Set speech speed (slow=False for normal speed)
slow = False

# Choose a TLD for influencing accent (e.g., .com.au for Australian)
tld = 'com'  # Adjust this for the desired accent (see examples below)

# Create the gTTS object
tts = gTTS(text=text, lang=language, slow=slow, tld=tld)

# Save the audio to a file (MP3 format by default)
tts.save("output.mp3")

print("Text converted to speech with", tld, "accent (may vary) and saved as output.mp3")
