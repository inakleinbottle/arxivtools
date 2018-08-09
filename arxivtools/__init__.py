#
import os
import json

import appdirs


OUTPUT_DIR = os.path.expanduser(os.path.join('~', 'arxiv'))
APP_CONF_DIR = appdirs.user_data_dir(__name__, '')





def daily_search():
    from arxivtools.rss import ArxivRSSFeed
    AF = ArxivRSSFeed(['math'])
    filtered_entries = AF.filter_all()
    for e in filtered_entries:
        with open(os.path.join(OUTPUT_DIR, e.arxiv_id + '.arx'), 'w') as f:
            json.dump(e, f)
