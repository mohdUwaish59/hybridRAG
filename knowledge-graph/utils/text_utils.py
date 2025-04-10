# utils/text_utils.py

def clean_text(text):
    """Clean the input text for processing."""
    text = text.replace("\n", " ").strip()
    return text
