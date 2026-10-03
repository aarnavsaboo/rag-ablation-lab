from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
import json


@dataclass(frozen=True)
class Document:
    id: str
    text: str


@dataclass(frozen=True)
class Query:
    id: str
    text: str
    relevant: frozenset[str]


@dataclass(frozen=True)
class Dataset:
    documents: tuple[Document, ...]
    queries: tuple[Query, ...]


def load(path: str) -> Dataset:
    data = json.loads(Path(path).read_text(encoding="utf-8"))
    documents = tuple(Document(str(x["id"]), str(x["text"])) for x in data["documents"])
    queries = tuple(
        Query(str(x["id"]), str(x["text"]), frozenset(str(v) for v in x["relevant"]))
        for x in data["queries"]
    )
    return Dataset(documents, queries)
