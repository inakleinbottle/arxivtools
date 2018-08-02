import requests
import feedparser



API = 'http://export.arxiv.org/api/query?'



class ArxivAPIRequest:

    def __init__(self, search_terms, id_list, max_records,
                 start_index, sort_by, sort_order):
        self.session = requests.Session()
        self.request = requests.Request().prepare()

    def make_request(self):
        return self.session.send(self.request)

    
