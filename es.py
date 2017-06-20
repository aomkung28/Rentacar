from elasticsearch import Elasticsearch
from elasticsearch_dsl import MultiSearch, Search
class dbe:
    def __init__(self):
        self.es = Elasticsearch([{'host': 'localhost', 'port': 9200}])
    def do_login(self):
        es.search(index="authentication", body={"query": {"bool": {
            "must": [{"term": {"password.keyword": "thailand"}}, {"term": {"email.keyword": "admin@admin.com"}}],
            "must_not": [], "should": []}}, "from": 0, "size": 10, "sort": [], "aggs": {}})

    def dsl(self):
        s = Search(using=self.es, index="authentication") \
            .filter("term", password="thailand") \
            .query("match", email="admin@admin.com")

        #s.aggs.bucket('per_tag', 'terms', field='tags') \
        #    .metric('max_lines', 'max', field='lines')
        response = s.execute()
        for hit in response:
            print hit

    def dsl2(self):
        s = Search(using=self.es, index="authentication")
        s.from_dict({"query": {"bool": {
            "must": [{"term": {"password.keyword": "thailand"}}, {"term": {"email.keyword": "admin@admin.com"}}],
            "must_not": [], "should": []}}, "from": 0, "size": 10, "sort": [], "aggs": {}})
        response = s.execute()
        for hits in response:
            print hits
if __name__ == '__main__':


    es = Elasticsearch([{'host': 'localhost', 'port': 9200}])

    ms = MultiSearch(using=es, index='authentication')

    ms = ms.add(Search().filter('term', password='thailand'))
    ms = ms.add(Search().filter('term', email='admin@admin.com'))

    responses = ms.execute()

    for response in responses:
        for hit in response:
            print(hit)

