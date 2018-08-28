
from collections import namedtuple


import re

from bs4 import BeautifulSoup


ENTRY_RE = re.compile(r'(?:[aA]r[xX]iv:)?'
                      r'(?P<arxiv_id>(\d{4}[.]\d{4,5})|([a-zA-Z-]+\/\d{,7}))'
                      r'(v(?P<version>\d+))?')


def sanitise(data):
    soup = BeautifulSoup(data, features='html5lib')
    return soup.get_text().replace('\n', ' ').strip()

ArxivEntry = namedtuple('ArxivEntry', ('authors', # Tuple of authors
                                       'arxiv_id', # Arxiv id
                                       'title', # Title of the article
                                       'abstract', # Complete abstract
                                       'version', # version
                                       ))



def make_entry(data):
    '''Make an ArxivEntry data from the provided information as dictionary.'''
    aid = data.get('arxiv_id')
    
    # Extract the version information from the id
    match = ENTRY_RE.search(aid)
    if match:
        data.update(match.groupdict())
    else:
        raise ValueError('Invalid ArXiv ID format')
    
    return ArxivEntry(**data)
    
    
