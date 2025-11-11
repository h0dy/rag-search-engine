from .search_utils import tokenize_text
from .utils import load_movies, save_cache, load_cache
from collections import defaultdict, Counter
import math

class InvertedIndex:
  # dictionary mapping tokens (strings) to sets of document IDs
  index = defaultdict(set)

  # dictionary mapping document IDs to their full document objects
  docmap: dict[int, dict] = {} 

  term_frequencies: dict[int, Counter] = {}

  def __add_document(self, doc_id: int, text: str) -> None:
    tokenized_text = tokenize_text(text)
    
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
  
  # load loads cache from cache folder to InvertedIndex attributes
  def load(self) -> None:
    InvertedIndex.index = load_cache("index")
    InvertedIndex.docmap = load_cache("docmap")
    InvertedIndex.term_frequencies = load_cache("term_frequencies")
  
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