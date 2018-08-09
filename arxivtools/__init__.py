
import os
import json
import logging

import appdirs

from arxivtools.entries import ArxivEntry
from arxivtools.filter import Filter, SimpleNBFilter
from arxivtools.rss import ArxivRSSFeed

__all__ = ['ArxivEntry', 'Filter', 'SimpleNBFilter',
           'ArxivRSSFeed', 'daily_search']


OUTPUT_DIR = os.path.expanduser(os.path.join('~', 'arxiv'))
APP_CONF_DIR = appdirs.user_data_dir(__name__, '')

logger = logging.getLogger()
#logger.basicConfig(level=logging.DEBUG)
log_path = os.path.join(APP_CONF_DIR, 'arxivtools.log')
log_file_handler = logging.FileHandle(log_path)
log_file_handler.setLevel(logging.DEBUG)
logger.addHandler(log_file_handler)




def daily_search():
    from arxivtools.rss import ArxivRSSFeed
    topics = ['math']
    AF = ArxivRSSFeed(topics)
    logger.info('Searching Daily RSS feed for topics: %s' % ', '.join(topics))
    filtered_entries = AF.filter_all()
    for e in filtered_entries:
        with open(os.path.join(OUTPUT_DIR, e.arxiv_id + '.arx'), 'w') as f:
            json.dump(e, f)
