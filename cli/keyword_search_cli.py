#!/usr/bin/env python3

import argparse
from lib.search_command import search_movie_command 
from lib.build_command import build_command
from lib.tf_command import calculate_tf
from lib.idf_command import calculate_idf
from lib.tf_idf_command import calculate_tf_idf

def main() -> None:
    parser = argparse.ArgumentParser(description="Keyword Search CLI")
    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    subparsers.add_parser("build", help="Build inverted index for faster search")

    tf_parser = subparsers.add_parser("tf", help="Return term frequency for a given document ID and term")
    tf_parser.add_argument("doc_id", type=str, help="Document ID")
    tf_parser.add_argument("term", type=str, help="Term to get frequency")

    search_parser = subparsers.add_parser("search", help="Search movies using BM25")
    search_parser.add_argument("query", type=str, help="Search query")

    idf_parser = subparsers.add_parser("idf", help="Get inverse document frequency for a given term")
    idf_parser.add_argument("term", type=str, help="Term to get inverse document frequency")

    tfidf_parser = subparsers.add_parser("tfidf", help="Get term frequency * inverse document frequency for a given document ID and term")
    tfidf_parser.add_argument("doc_id", type=str, help="Document ID")
    tfidf_parser.add_argument("term", type=str, help="Term to TF-IDF")

    args = parser.parse_args()
    match args.command:
        case "build":
           print("building inverted index.....")
           build_command()

        case "search":
            query_search = args.query
            print(f"Searching for: {query_search}...\n")

            movie_results = search_movie_command(query=query_search)
            movie_results.sort(key=lambda e: e["id"])

            for idx, mr in enumerate(movie_results, start=1):
                print(f"{idx}. {mr["title"]}")
        case "tf":
            term = args.term
            doc_id = int(args.doc_id)
            term_counter = calculate_tf(term, doc_id)
            print(f"Term frequency of '{term}' in document '{doc_id}': {term_counter}")
        
        case "idf":
            term = args.term
            idf = calculate_idf(term)
            print(f"Inverse document frequency of '{term}': {idf:.2f}")
        
        case "tfidf":
            term = args.term
            doc_id = int(args.doc_id)
            tf_idf = calculate_tf_idf(term, doc_id)
            print(f"TF-IDF score of '{term}' in document '{doc_id}': {tf_idf:.2f}")
        case _:
            parser.print_help()
    print()


if __name__ == "__main__":
    main()