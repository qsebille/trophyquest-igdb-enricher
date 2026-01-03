import math
import re


def normalize(s: str) -> str:
    s = s.lower().strip()
    s = re.sub(r"[^a-z0-9 ]+", " ", s)
    s = re.sub(r"\s+", " ", s)
    return s


def tokens(s: str) -> list[str]:
    return normalize(s).split(" ")
    # TODO: remove stop words


# Calcul du score F1 (précision/rappel) de matching avec floor
def compute_candidate_score(query: str, candidate: str) -> int:
    if normalize(query) == normalize(candidate):
        return 100

    intersection = len(set(tokens(query)).intersection(set(tokens(candidate))))
    precision = intersection / len(tokens(query))
    recall = intersection / len(tokens(candidate))
    f1_score = 0 if intersection == 0 else (2 * precision * recall) / (precision + recall)

    return math.floor(f1_score * 100)
