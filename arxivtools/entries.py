
from collections import namedtuple


from bs4 import BeautifulSoup

def sanitise(data):
    soup = BeautifulSoup(data, features='html5lib')
    return soup.get_text().replace('\n', ' ').strip()

ArxivEntry = namedtuple('ArxivEntry', ('authors', 'arxiv_id', 'title', 'abstract'))

#@dataclass(frozen=True)
#class ArxivEntry:
#    authors: tuple
#    arxiv_id: str
#    title: str
#    abstract: str
#    #updated: str
