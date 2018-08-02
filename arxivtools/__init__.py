
from .filter import Filter, get_filter

from dataclasses import dataclass

@dataclass
class ArxivEntry:
    authors: tuple
    arxiv_id: str
    title: str
    abstract: str
    #updated: str

