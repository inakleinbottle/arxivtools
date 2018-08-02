
from dataclasses import dataclass




@dataclass(frozen=True)
class ArxivEntry:
    authors: tuple
    arxiv_id: str
    title: str
    abstract: str
    #updated: str
