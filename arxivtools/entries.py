
from collections import namedtuple


import re

from bs4 import BeautifulSoup

def sanitise(data):
    soup = BeautifulSoup(data, features='html5lib')
    return soup.get_text().replace('\n', ' ').strip()

ArxivEntry = namedtuple('ArxivEntry', ('authors', # Tuple of authors
                                       'arxiv_id', # Arxiv id
                                       'title', # Title of the article
                                       'abstract', # Complete abstract
                                       'version', # version
                                       ))

#@dataclass(frozen=True)
#class ArxivEntry:
#    authors: tuple
#    arxiv_id: str
#    title: str
#    abstract: str
#    #updated: str



def make_entry(data):
    '''Make an ArxivEntry data from the provided information as dictionary.'''
    aid = data.get('arxiv_id')
    
    # Extract the version information from the id
    match = re.match(r'(?<arid>\d{4}[.]\d{4,5})(?<vers>v\d+)?|'
                     r'(?<arid>[a-zA-Z-/]+\d{4,5})(?<vers>v\d+)?',
                     aid)
    if match:
        try:
            vers = int(match.group('vers').strip('v'))
        except IndexError:
            vers = 1
        arxiv_id = match.group('arid')
    else:
        raise ValueError('Invalid ArXiv ID format')
    
    return ArxivEntry(data.get('authors'),
                      arxiv_id,
                      data.get('title'),
                      data.get('abstract')
                      vers
                      )
    
    