#!/usr/bin/env python3

import argparse
from lib.search_command import search_movie_command 
from lib.build_command import build_command

def main() -> None:
    parser = argparse.ArgumentParser(description="Keyword Search CLI")
    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    subparsers.add_parser("build", help="Build inverted index for faster search")
    search_parser = subparsers.add_parser("search", help="Search movies using BM25")
    search_parser.add_argument("query", type=str, help="Search query")

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
            
            # print the search query here
            pass
        case _:
            parser.print_help()
    print()


if __name__ == "__main__":
    main()