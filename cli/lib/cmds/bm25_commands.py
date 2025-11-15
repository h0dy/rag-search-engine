from lib.inverted_index import InvertedIndex

DEFAULT_SEARCH_LIMIT = 5

def bm25_idf_command(term: str) -> float:
  idx = InvertedIndex() 
  idx.load()
  bm25_idf_score = idx.get_bm25_idf(term)
  return bm25_idf_score

def bm25_tf_command(term: str, doc_id: int, k1, b) -> float:
  idx = InvertedIndex()
  idx.load()
  bm25_tf_score = idx.get_bm25_tf(doc_id, term, k1, b)
  return bm25_tf_score

def bm25_search_command(query: str, limit: int = DEFAULT_SEARCH_LIMIT) -> list[dict]:
  idx = InvertedIndex()
  idx.load()
  return idx.bm25_search(query, limit)