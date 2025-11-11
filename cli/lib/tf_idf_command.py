from .inverted_index import InvertedIndex
from .idf_command import calculate_idf
from .tf_command import calculate_tf

def calculate_tf_idf(term: str, doc_id: int) -> float:
  tf = calculate_tf(term, doc_id)
  idf = calculate_idf(term)
  return tf * idf 