from .search_utils import tokenize_text
from .utils import load_movies, save_cache, load_cache
from collections import defaultdict, Counter

class InvertedIndex:
  # dictionary mapping tokens (strings) to sets of document IDs
  index = defaultdict(set)

  # dictionary mapping document IDs to their full document objects
  docmap: dict[int, dict] = {}

  def __add_document(self, doc_id: int, text: str) -> None:
    tokenized_text = tokenize_text(text)
    for token in tokenized_text:
      InvertedIndex.index.setdefault(token, set()).add(doc_id)
      InvertedIndex.term_frequencies[token["id"]] += 1
  
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

  def save(self) -> None:
    save_cache(InvertedIndex.docmap, "docmap")
    save_cache(InvertedIndex.index, "index")
    save_cache(InvertedIndex.term_frequencies, "term_frequencies")
  
  def load(self) -> None:
    InvertedIndex.index = load_cache("index")
    InvertedIndex.docmap = load_cache("docmap")
    InvertedIndex.term_frequencies = load_cache("term_frequencies")
 