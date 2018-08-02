
import feedparser

from . import ArxivEntry

API = 'http://arxiv.org/rss/'


class ArxivRSSFeed:

    def __init__(self, topics):
        self.topics = topics

    def get(self):
        pass
        
