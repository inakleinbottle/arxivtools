import logging

import pickle
import os
from abc import ABC

import numpy as np
from sklearn.datasets import load_files
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.pipeline import make_pipeline

from arxivtools import APP_CONF_DIR


logger = logging.getLogger(__name__)

class PipeLine():
    filters = []

    def update(self, path):
        for filt in self.filters:
            filt.update(path)
        

    def apply(self,data):
        res = False
        for filt in self.filters:
            res |= filt.apply(data)
        return res

    def add_filter(self, filt):
        self.filters.append(filt)

    def rem_filter(self, flt):
        try:
            self.filters.remove(flt)
        except ValueError:
            pass

class Filter(ABC):

    def _select_data(self, entry):
        return entry

    def update(self, path):
        logger.debug('Loading new training data and training model')
        training_data = load_files(path)
        text, target = training_data.data, training_data.target
        self.predictor.fit(text, target)

    def apply(self, entry):
        result = bool(self.predictor.predict(self._select_data(entry)))
        logger.info('Entry %s, result %s' % (entry.arxiv_id, result))
        return result


class AuthorPredictor:

    def __init__(self):
        import csv
        authors = []
        with open(os.path.join(APP_CONF_DIR, 'authors.csv'), 'r') as f:
            for row in csv.reader(f):
                authors.append(row)
        self.authors = authors

    def predict(self, authors):
        return any(au in self.authors for au in authors)

    def fit(self, data, target):
        pass
        

class AuthorFilter(Filter):
    def __init__(self):
        self.predictor = AuthorPredictor()

    def _select_data(self, entry):
        return entry.authors
    


class SimpleNBFilter(Filter):

    def __init__(self):
        self.predictor = make_pipeline(CountVectorizer(ngram_range=(1,3),
                                                       stop_words='english'),
                                       MultinomialNB())

    def _select_data(self, entry):
        return [entry.abstract]



class DefaultPipeline(PipeLine):
    _filters = [AuthorFilter, SimpleNBFilter]

    def __init__(self):
        self.filters = [filt() for filt in self._filters]




def get_filter(path):
    filter_path = os.path.join(path, 'default.flt')
    if not os.path.exists(filter_path):
        logger.warning('Default filter not found, creating new filter')
        return new_filter(path)
    else:
        logger.debug('Loading default filter from %s' % filter_path)
        with open(filter_path, 'rb') as f:
            return pickle.load(f)

def new_filter(path, cls=None):
    logger.debug('Creating new %s as default filter' % DefaultPipeline.__name__)
    if not cls:
        filt = DefaultPipeline()
    else:
        filt = cls()
        
    data_path = os.path.join(path, 'data')
    filt.update(data_path)
    with open(os.path.join(path, 'default.flt'), 'wb') as f:
        pickle.dump(filt, f)
        
    return filt
