
import re
import logging
import json

import feedparser



from arxivtools import APP_CONF_DIR
from arxivtools.filter import get_filter
from arxivtools.entries import make_entry, sanitise


logger = logging.getLogger(__name__)

AUTHOR_RE = re.compile(r',\s*(?![^()]*\))')

def extract_authors(authors):
    for au in authors:
        yield from AUTHOR_RE.split(sanitise(au.name))







API = 'http://arxiv.org/rss/'


class ArxivRSSFeed:

    def __init__(self, topics):
        self.topics = topics
        self._cached_ids = set()
        self._cache = []
        self.accepted = []
        self.rejected = []

    def get_topic(self, topic):
        logger.debug('Retrieving feed for %s' % topic)
        feed = feedparser.parse(API + topic)
        logger.info('Found %s entries on topic %s' % (len(feed.entries), topic))
        for entry in feed.entries:
            item = make_entry({'authors' : tuple(extract_authors(entry.authors)),
                               'arxiv_id' : entry.id.split('/abs/')[-1].strip(),
                               'title' : entry.title.strip(),
                               'abstract' : sanitise(entry.summary)})
            if item.arxiv_id in self._cached_ids:
                continue
            else:
                self._cache.append(item)
                self._cached_ids.add(item.arxiv_id)
                yield item

    def get_all(self):
        logger.debug('Retrieving all entries for topics: %s' % ', '.join(self.topics))
        if self._cache:
            yield from iter(self._cache)
        else:
            for topic in self.topics:
                yield from self.get_topic(topic)

    def filter_all(self):
        filt = get_filter(APP_CONF_DIR)
        logger.debug('Filtering results using default filter')
        all_entries = self.get_all()
        for entry, status in zip(all_entries, map(filt.apply, all_entries)):
            if status:
                self.accepted.append(entry)
                yield entry
            else:
                self.rejected.append(entry)

    def dump_rejected(self, fd):
        for item in self.rejected:
            json.dump(item, fd, sort_keys=True, indent =4)


