import csv

import requests
import feedparser
import os.path as osp

#from arxivtools import APP_CONF_DIR
from arxivtools.entries import make_entry, sanitise

import appdirs

API = 'http://export.arxiv.org/api/query?'
APP_CONF_DIR = appdirs.user_data_dir('arxivtools', '')


class ArxivAPIRequest:

    def __init__(self, search_terms=None, id_list=None,
                 max_records=100, start_index=0,
                 sort_by='lastUpdatedDate', sort_order='ascending'):
        self.query = (f'''{"search_query=" + " OR ".join(
                          f'{k}:"{i}"' for k, v in search_terms.items()
                          for i in v) + "&" if search_terms else ""}'''
                      f'''{"id_list=" + ",".join(id_list) + "&" if id_list
                           else ""}'''
                      f'''max_results={max_records}&'''
                      f'''sortBy={sort_by}&'''
                      f'''sortOrder={sort_order}''')
        

    def make_request(self):
        feed = feedparser.parse(requests.get(API + self.query).text)
        for entry in feed.entries:
            yield make_entry({'authors' : tuple(au.name for au in entry.authors),
                              'arxiv_id' : entry.id.split('/abs/')[-1].strip(),
                              'title' : entry.title.strip(),
                              'abstract' : sanitise(entry.summary)})


def learn_authors():
    with open(osp.join(APP_CONF_DIR, 'authors.csv'), 'r') as f:
        authors = []
        for row in csv.reader(f):
            authors.extend(row)
        get_preferred_authors(authors)
        

def get_preferred_authors(authors):
    AF = ArxivAPIRequest({'au' : authors})
    for entry in AF.make_request():
        path = entry.arxiv_id.replace('/','-')
        with open(osp.join(APP_CONF_DIR, 'data', 'pos', path), 'w') as f:
            f.write(entry.abstract)
        
