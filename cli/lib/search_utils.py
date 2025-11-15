from .utils import load_stop_words
from nltk.stem import PorterStemmer
from typing import Any
import string

SCORE_PRECISION = 3

def has_matching_token(query_tokens: list[str], title_tokens: list[str]) -> bool:
    for q in query_tokens:
        for t in title_tokens:
            if q in t:
                return True
    return False

# remove punctuation
def preprocess_text(text: str) -> list[str]:
    text = text.lower() # lower the text
    text = text.translate(str.maketrans("", "", string.punctuation)) 
    return text

# Tokenization
def tokenize_text(text:  str)  -> list[str]:
    text = preprocess_text(text)
    tokens = text.split()
    valid_tokens = []
    
    for token in tokens:
        if token:
            valid_tokens.append(token)

    # filtering stop words
    filtered_tokens = []
    stop_words = load_stop_words()
    for token in valid_tokens:
        if token not in stop_words:
            filtered_tokens.append(token)

    # steaming
    steamed_tokens = []
    steamer = PorterStemmer()
    for token in filtered_tokens:
        steamed_tokens.append(steamer.stem(token)) 
    
    return steamed_tokens

def format_search_result(
    doc_id: str, title: str, document: str, score: float, **metadata: Any
) -> dict[str, Any]:
    """Create standardized search result

    Args:
        doc_id: Document ID
        title: Document title
        document: Display text (usually short description)
        score: Relevance/similarity score
        **metadata: Additional metadata to include

    Returns:
        Dictionary representation of search result
    """
    return {
        "id": doc_id,
        "title": title,
        "document": document,
        "score": round(score, SCORE_PRECISION),
        "metadata": metadata if metadata else {},
    }