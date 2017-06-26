from elasticsearch import Elasticsearch
from elasticsearch_dsl import MultiSearch, Search
import requests
import json
class db:
    def __init__(self):
        self.es = Elasticsearch([{'host': 'localhost', 'port': 9200}])

    def _OLDdo_login(self, username, password):
        # type: (str, str) -> [] or str
        ms = MultiSearch(using=self.es, index='authentication')
        ms = ms.add(Search().filter('term', password=password))
        ms = ms.add(Search().filter('term', email=username))
        records = ms.execute()
        _isin = False
        for response in records:
            if response:
                _isin = True

                return response[0]
            else:
                return False

    def profile(self, id):

        pass
    def login(self, username, password):
        res = self.es.search(index="account", body=
        {"query": {"bool": {
            "must": [{"match": {"account.email": username}},
                     {"match": {"account.password": password}},
                     {"match": {"account.isAdmin": True}},
                     {"match": {"account.isActive": True}}]}},
            "size": 1})

        if res['hits']['total'] > 0:
            return res['hits']['hits'][0]
        else:
            return False

    def do_login(self, username, password):
        res = self.es.post(index="account", body=
        {"query": {"bool": {
            "must": [{"match": {"account.email": username}},
                     {"match": {"account.password": password}},
                     {"match": {"account.isAdmin": True}},
                     {"match": {"account.isActive": True}}]}},
            "size": 1})
        print res
        if res['hits']['total'] > 0:
            return res['hits']['hits'][0]
        else:
            return False

    def get_report_datatable(self):
        datatable = self.es.search(index="deals", body={"query": {"bool": {"must": [{"match_all": {}}]}}}, size=100)
        #print json.dumps(datatable)
        if datatable['hits']['total'] > 0:
            return datatable['hits']['hits']
        else:
            return False

    def get_customers_datatable(self):
        datatable = self.es.search(index="deals", body={"query":{"bool":{"must":[{"term":{"deal.isRecurring":"true"}}],"must_not":[],"should":[]}}}, size=100)
        #print json.dumps(datatable)
        if datatable['hits']['total'] > 0:
            return datatable['hits']['hits']
        else:
            return False

    def get_all_recurring_datatable(self):
        datatable = self.es.search(index="deals", body={"query": {"bool": {"must": [{"match_all": {}}]}}}, size=100)
        #print json.dumps(datatable)
        if datatable['hits']['total'] > 0:
            return datatable['hits']['hits']
        else:
            return False
if __name__ == '__main__':
    AFD = db()
    for elem in AFD.do_report_datatable():
        print 'customer', elem['_source']['customer']
        print 'deal', elem['_source']['deal']