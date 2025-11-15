from ..inverted_index import InvertedIndex

def calculate_idf(term: str) -> float:
  idx = InvertedIndex()
  idx.load()
  return idx.get_idf(term)