
from collections import namedtuple


ArxivEntry = namedtuple('ArxivEntry', ('authors', 'arxiv_id', 'title', 'abstract'))

#@dataclass(frozen=True)
#class ArxivEntry:
#    authors: tuple
#    arxiv_id: str
#    title: str
#    abstract: str
#    #updated: str
