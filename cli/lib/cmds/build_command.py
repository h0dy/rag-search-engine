from ..inverted_index import InvertedIndex

def build_command() -> None:
    inverted_idx = InvertedIndex()
    inverted_idx.build()
    inverted_idx.save()
    docs = inverted_idx.get_documents("merida")
    print(f"First document for token 'merida' = {docs[0]}")