import re
import spacy

# Load spaCy model for Polish
nlp_pl = spacy.load("pl_core_news_lg")

# Function to analyze a cleaned Polish word
def analyze_cleaned_polish_word(word):
    # Define a pattern to remove specific characters
    pattern = r'[@\(\)>;:".,?!„”]'  # Add more characters inside the brackets if needed
    cleaned_word = re.sub(pattern, '', word)
    
    # Analyze the cleaned word with spaCy
    doc_pl = nlp_pl(cleaned_word)
    
    # Get lemma, POS, and morphological description
    analyzed_word = None
    for token in doc_pl:
        lemma = token.lemma_
        pos = token.pos_
        morph_description = token.morph
        analyzed_word = (cleaned_word, lemma, pos, morph_description)
    
    return analyzed_word

# Example word
word_pl = "danych”."

# Analyze the cleaned Polish word
analyzed_word = analyze_cleaned_polish_word(word_pl)
if analyzed_word:
    word, lemma, pos, morph_description = analyzed_word
    print(f"Original Word: {word}, Lemma: {lemma}, POS: {pos}, Morph: {morph_description}")
else:
    print("Word could not be analyzed.")
