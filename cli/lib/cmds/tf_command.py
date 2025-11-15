from lib.inverted_index import InvertedIndex

def calculate_tf(term: str, doc_id: int) -> int:
  idx = InvertedIndex()
  idx.load()
  counter = idx.get_tf(doc_id, term)
  return counter
