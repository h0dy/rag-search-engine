from ..inverted_index import InvertedIndex
from ..search_utils import tokenize_text

    
def search_movie_command(query: str, limit: int = 5) -> list[dict]:
    inverted_idx = InvertedIndex()
    inverted_idx.load()
    query_tokens = tokenize_text(query)

    seen, results = set(), []
    for token in query_tokens:
        doc_ids = inverted_idx.get_documents(token)
        if doc_ids == None:
            continue
        for doc_id in doc_ids:
            if doc_id in seen:
                continue
            seen.add(doc_id)
            results.append(inverted_idx.docmap[doc_id])
            if len(results) >= limit:
                return results
    return results



