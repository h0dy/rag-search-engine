from .search_utils import tokenize_text, format_search_result
from .utils import load_movies, save_cache, load_cache
from collections import defaultdict, Counter
import math

BM25_K1 = 1.5
BM25_B = 0.75

class InvertedIndex:
  # dictionary mapping tokens (strings) to sets of document IDs
  index = defaultdict(set)

  # dictionary mapping document IDs to their full document objects
  docmap: dict[int, dict] = {}

  term_frequencies: dict[int, Counter] = {}
  
  doc_lengths: dict[int, int] = {}

  def __get_avg_doc_length(self) -> float:
    doc_count = len(InvertedIndex.docmap)

    if doc_count == 0:
        return 0.0

    total_doc_lengths = sum(InvertedIndex.doc_lengths.values())
    return total_doc_lengths / doc_count
    
  def __add_document(self, doc_id: int, text: str) -> None:
    tokenized_text = tokenize_text(text)
    InvertedIndex.doc_lengths[doc_id] = len(tokenized_text)
    
    if doc_id not in InvertedIndex.term_frequencies:
      InvertedIndex.term_frequencies[doc_id] = Counter()
    
    for token in tokenized_text:
      InvertedIndex.index.setdefault(token, set()).add(doc_id)
      InvertedIndex.term_frequencies[doc_id][token] += 1
  
  def get_documents(self, term: str) -> list[int]:
    term = term.lower()
    doc_ids = InvertedIndex.index.get(term, set())
    return sorted(list(doc_ids))

  def build(self) -> None:
    movies = load_movies()
    for m in movies:
      movie_token = f"{m['title']} {m['description']}"
      self.__add_document(m["id"], movie_token)
      InvertedIndex.docmap[m["id"]] = m

  # save saves obj using pkl into cache folder
  def save(self) -> None:
    save_cache(InvertedIndex.docmap, "docmap")
    save_cache(InvertedIndex.index, "index")
    save_cache(InvertedIndex.term_frequencies, "term_frequencies")
    save_cache(InvertedIndex.doc_lengths, "doc_lengths")
  
  # load loads cache from cache folder to InvertedIndex attributes
  def load(self) -> None:
    InvertedIndex.index = load_cache("index")
    InvertedIndex.docmap = load_cache("docmap")
    InvertedIndex.term_frequencies = load_cache("term_frequencies")
    InvertedIndex.doc_lengths = load_cache("doc_lengths")
  
  # get_tf returns how often a term appears in a given document ID
  def get_tf(self, doc_id: int, term: str) -> str:
    term = term.lower()
    tokenized_term = tokenize_text(term)
    if len(tokenized_term) > 1:
      raise ValueError("term shouldn't be more than one word")

    term_counter = self.term_frequencies.get(doc_id)
    if not term_counter:
      raise KeyError(f"Document {doc_id} not found")

    return term_counter[tokenized_term[0]]

  # get_idf returns how rare a term is across all documents
  def get_idf(self, term: str) -> float:
    tokens = tokenize_text(term)
    if len(tokens) != 1:
      raise ValueError("term shouldn't be more than one word")
    
    doc_count = len(InvertedIndex.docmap)
    term_doc_count = len(self.get_documents(tokens[0]))
    idf = math.log((doc_count + 1) / (term_doc_count + 1))
    return idf

  def get_bm25_idf(self, term: str) -> float:
    tokens = tokenize_text(term)
    if len(tokens) != 1:
      raise ValueError("term shouldn't be more than one word")
    
    doc_count = len(InvertedIndex.docmap)
    df = len(self.get_documents(tokens[0]))
    bm25 = math.log((doc_count - df + 0.25) / (df + 0.5) + 1)
    return bm25

  def get_bm25_tf(self, doc_id: int, term: str, k1 = BM25_K1, b = BM25_B) -> float:
    doc_length = InvertedIndex.doc_lengths[doc_id]
    avg_doc_length = self.__get_avg_doc_length()
    length_norm = 1 - b + b * (doc_length / avg_doc_length)

    tf  = self.get_tf(doc_id, term)
    tf_component = (tf * (k1 + 1)) / (tf + k1 * length_norm)
    return tf_component
  
  def bm25(self, doc_id, term) -> int:
    bm25_idf = self.get_bm25_idf(term)
    bm25_tf = self.get_bm25_tf(doc_id, term)
    return bm25_idf * bm25_tf
  
  def bm25_search(self, query, limit) -> list[dict]:
    tokenized_query = tokenize_text(query)

    bm25_scores: dict[int, int] = {}
    for doc_id in InvertedIndex.docmap:
      total = 0
      for term in tokenized_query:
        total += self.bm25(doc_id, term)
      bm25_scores[doc_id] = total

      sorted_docs = sorted(bm25_scores.items(), key=lambda x: x[1], reverse=True)

      results = []
      for doc_id, score in sorted_docs[:limit]:
        doc = self.docmap[doc_id]
        formatted_result = format_search_result(
          doc_id=doc["id"],
          title=doc["title"],
          document=doc["description"],
          score=score,
        )
        results.append(formatted_result)

    return results
