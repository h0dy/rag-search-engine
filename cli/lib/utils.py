import json
import os
import pickle as pkl

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
DATA_PATH = os.path.join(PROJECT_ROOT, "data", "movies.json")
STOPWORDS_PATH = os.path.join(PROJECT_ROOT,  "data", "stopwords.txt")


def load_movies() -> list[dict]:
    with open(DATA_PATH, "r") as f:
        movies = json.load(f)["movies"]
    return movies


def load_stop_words() -> list[str]:
    with open(STOPWORDS_PATH, "r") as f:
        stop_words = f.read().splitlines()
    return stop_words

def save_cache(obj: dict, file_name: str) -> None:
    path = os.path.join(PROJECT_ROOT,  "cache", f"{file_name}.pkl")
    with open(path, "wb") as f:
       pkl.dump(obj, f)

def load_cache(file_name: str) -> dict:
    path = os.path.join(PROJECT_ROOT,  "cache", f"{file_name}.pkl")
    with open(path, "rb") as f:
        data = pkl.load(f)
    return data
