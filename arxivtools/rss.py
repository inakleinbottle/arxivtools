
import re

import feedparser

from bs4 import BeautifulSoup

from arxivtools import APP_CONF_DIR
from arxivtools.filter import get_filter
from arxivtools.entries import ArxivEntry


AUTHOR_RE = re.compile(r',\s*(?![^()]*\))')

def extract_authors(authors):
    for au in authors:
        yield from AUTHOR_RE.split(sanitise(au.name))



def sanitise(data):
    soup = BeautifulSoup(data, features='html5lib')
    return soup.get_text().replace('\n', ' ').strip()



API = 'http://arxiv.org/rss/'


class ArxivRSSFeed:

    def __init__(self, topics):
        self.topics = topics
        self._cached_ids = set()
        self._cache = []

    def get_topic(self, topic):
        feed = feedparser.parse(API + topic)
        for entry in feed.entries:
            item = ArxivEntry(tuple(extract_authors(entry.authors)),
                              entry.id.split('/abs/')[-1].strip(),
                              entry.title.strip(),
                              sanitise(entry.summary))
            if item.arxiv_id in self._cached_ids:
                continue
            else:
                self._cache.append(item)
                self._cached_ids.add(item.arxiv_id)
                yield item

    def get_all(self):
        if self._cache:
            yield from iter(self._cache)
        else:
            for topic in self.topics:
                yield from self.get_topic(topic)

    def filter_all(self):
        filt = get_filter(APP_CONF_DIR)
        yield from filter(lambda t: filt.apply(t), self.get_all())



