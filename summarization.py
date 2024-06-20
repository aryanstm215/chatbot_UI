from transformers import pipeline

# Load the pre-trained summarization model and tokenizer
summarizer = pipeline('summarization')

# Define the text you want to summarize
text = """
This is a long article about artificial intelligence and its potential impact on society. Artificial intelligence (AI) has made significant strides in recent years, with breakthroughs in areas such as machine learning, natural language processing, and computer vision. However, the rapid advancement of AI has also raised concerns about its potential risks, including job displacement, privacy issues, and the possibility of AI systems becoming too powerful or uncontrollable.

One of the key challenges with AI is ensuring that it remains safe, ethical, and beneficial to humanity. There are ongoing debates about the need for proper governance frameworks, regulatory measures, and ethical guidelines to govern the development and deployment of AI systems. Additionally, there are concerns about the potential for AI to perpetuate or amplify existing biases and inequalities present in the data used to train these systems.

Despite these challenges, AI also holds immense potential for solving complex problems and improving various aspects of society. AI-powered systems are being employed in fields like healthcare, education, transportation, and environmental conservation, with the potential to revolutionize these areas and improve human lives.

As AI continues to evolve, it is crucial for policymakers, researchers, and the broader public to remain engaged in discussions about its responsible development and use. Striking the right balance between harnessing the benefits of AI while mitigating its risks will be a critical challenge in the years to come.
"""

# Generate a summary of the text
summary = summarizer(text, max_length=130, min_length=30, do_sample=False)[0]['summary_text']

# Print the summary
print(summary)