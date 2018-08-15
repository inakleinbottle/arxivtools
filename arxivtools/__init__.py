
import os
import json
import logging
import datetime
import shutil

from tempfile import TemporaryDirectory

import appdirs

__all__ = ['ArxivEntry', 'Filter', 'SimpleNBFilter',
           'ArxivRSSFeed', 'daily_search', 'OUTPUT_DIR',
           'APP_CONF_DIR']

OUTPUT_DIR = os.path.expanduser(os.path.join('~', 'arxiv'))
APP_CONF_DIR = appdirs.user_data_dir(__name__, '')

if not os.path.exists(OUTPUT_DIR):
    os.makedirs(OUTPUT_DIR)
if not os.path.exists(APP_CONF_DIR):
    os.makedirs(APP_CONF_DIR)

from arxivtools.entries import ArxivEntry
from arxivtools.filter import Filter, SimpleNBFilter
from arxivtools.rss import ArxivRSSFeed

logger = logging.getLogger('arxivtools')
logger.setLevel(logging.DEBUG)
#logger.basicConfig(level=logging.DEBUG)
log_path = os.path.join(APP_CONF_DIR, 'arxivtools.log')
log_file_handler = logging.FileHandler(log_path)
log_file_handler.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s - %(message)s')
log_file_handler.setFormatter(formatter)
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

    # Dump the rejected entries to a separate file
    dump_path = os.path.join(OUTPUT_DIR, 'rejected')
    if not os.path.exists(dump_path):
        os.mkdir(dump_path)

    dump_file = os.path.join(dump_path, str(datetime.date.today()))
    logger.info('Dumping results and compressing to %s' % dump_file + '.tar.gz')

    # Initial storage in temporary directory, will be deleted after archiving
    with TemporaryDirectory() as tmpdir:
        tmpfile = os.path.join(tmpdir, str(datetime.date.today()))

        with open(tmpfile, 'w') as fd:
            AF.dump_rejected(fd)
            
        # compress with tar.gz to save disk space
        shutil.make_archive(dump_file, 'gztar',  tmpdir)
