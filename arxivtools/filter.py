import logging
from abc import ABC

from sklearn.datasets import load_files
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB

class Filter(ABC):

    def _apply(self, entry):
        pass

    def update(self):
        pass

    def apply(self, entries):
        _execute = self._apply
        yield from map(_execute, entries)




class SimpleNBFilter(Filter):

    def __init__(self):
        self.vect = CountVectorizer()
        self.model = MultinomialNb()
        

    def _apply(self, entry):
        return (entry,
                bool(self.model.predict(self.vect.transform(entry.abstract))))


    def update(self):
        pass

    def _train(self, path):
        training_data = load_files(path)
        text, target = training_data.data, training_data.target
        predictors = self.vect.fit_transform()
        self.model.fit(predictors, target)
        
