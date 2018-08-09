import logging

import pickle
import os
from abc import ABC

from sklearn.datasets import load_files
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.pipeline import make_pipeline

logger = logging.getLogger(__name__)

class Filter(ABC):
    pipeline = None

    def update(self, path):
        training_data = load_files(path)
        text, target = training_data.data, training_data.target
        self.pipeline.fit(text, target)

    def apply(self, entry):
        result = bool(self.pipeline.predict([entry.abstract]))
        logger.info(entry.arxiv_id, result)
        return result




class SimpleNBFilter(Filter):

    def __init__(self):
        self.pipeline = make_pipeline(CountVectorizer(ngram_range=(1,3),
                                                      stop_words='english'),
                                      MultinomialNB())


DEFAULT_FILTER = SimpleNBFilter

def get_filter(path):
    filter_path = os.path.join(path, 'default.flt')
    if not os.path.exists(filter_path):
        return new_filter(path)
    else:
        with open(filter_path, 'rb') as f:
            return pickle.load(f)

def new_filter(path, cls=None):
    if not cls:
        filt = DEFAULT_FILTER()
    else:
        filt = cls()
        
    data_path = os.path.join(path, 'data')
    filt.update(data_path)
    with open(os.path.join(path, 'default.flt'), 'wb') as f:
        pickle.dump(filt, f)
        
    return filt
