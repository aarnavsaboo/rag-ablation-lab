from collections import Counter
from math import log
import re

from .dataset import Document


def tokenize(text: str) -> list[str]:
    return re.findall(r"\w+", text.casefold())


class BM25Retriever:
    def __init__(self, documents: tuple[Document, ...], k1: float = 1.5, b: float = .75):
        self.documents = documents
        self.k1 = k1
        self.b = b
        self.counts = [Counter(tokenize(x.text)) for x in documents]
        self.lengths = [sum(x.values()) for x in self.counts]
        self.avg_length = sum(self.lengths) / max(1, len(self.lengths))
        df = Counter(term for counts in self.counts for term in counts)
        n = len(documents)
        self.idf = {term: log(1 + (n - freq + .5) / (freq + .5)) for term,freq in df.items()}

    def search(self, query: str, k: int) -> list[str]:
        terms = set(tokenize(query))
        rows = []
        for doc, counts, length in zip(self.documents, self.counts, self.lengths):
            score = 0.0
            for term in terms:
                tf = counts.get(term, 0)
                if not tf:
                    continue
                denom = tf + self.k1 * (1 - self.b + self.b * length / max(self.avg_length, 1e-9))
                score += self.idf.get(term, 0) * tf * (self.k1 + 1) / denom
            rows.append((doc.id, score))
        return [doc_id for doc_id,score in sorted(rows,key=lambda x:(-x[1],x[0]))[:k] if score > 0]
