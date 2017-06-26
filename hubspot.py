import requests
import json
import elasticsearch_dsl
from  elasticsearch import Elasticsearch
import datetime
import os
import stripe
stripe.api_key = "sk_test_KJK0UUP60sTjJ0hR5TmbqbGU"
class api_hub:
    def __init__(self):
        self.es = Elasticsearch([{'host': 'localhost', 'port': 9200}])
    def fetch(self, url):
        req = requests.get(url)
        if req.status_code == 200:
            return json.loads(req.content)
        else:
            return False
    def get_all_deals(self):
        deals = self.fetch('https://api.hubapi.com/deals/v1/deal/paged?hapikey=a17334e9-ca7c-4df9-b763-371c280399ee&properties=dealname&properties=amount&properties=closedate')
        for e in deals['deals']:
            try:
                dd = e['properties']['closedate']['value']
                date = datetime.datetime.fromtimestamp(long(dd)/1000).strftime('%Y-%m-%d %H:%M:%S')
                print date
            except KeyError:
                print ''
        return deals
    def get_contact(self, id):
        contact = self.fetch('https://api.hubapi.com/contacts/v1/contact/vid/{}/profile?hapikey=a17334e9-ca7c-4df9-b763-371c280399ee&properties=email&properties=lastname&properties=firstname&properties=company'.format(id))
        data = dict()
        try:
            data['firstname'] = contact['properties']['firstname']['value']
        except KeyError:
            data['firstname'] = ''
        try:
            data['lastname'] = contact['properties']['lastname']['value']
        except KeyError:
            data['lastname'] = ''
        try:
            data['company'] = contact['properties']['company']['value']
        except KeyError:
            data['company'] = ''
        try:
            data['email'] = contact['properties']['email']['value']
        except KeyError:
            data['email'] = ''

        return data
    def get_all_pipelines(self):
        F = open('deal.txt', 'w')

        i = 0
        hasMore = True
        offset = False
        while hasMore == True:
            if offset != False:
                deals = self.fetch('https://api.hubapi.com/deals/v1/deal/paged?hapikey=a17334e9-ca7c-4df9-b763-371c280399ee&properties=dealname&properties=amount&properties=dealstage&properties=dealtype&properties=num_associated_contacts&properties=closedate&offset={}'.format(offset))
                offset = deals['offset']
                hasMore = deals['hasMore']
            else:
                deals = self.fetch('https://api.hubapi.com/deals/v1/deal/paged?hapikey=a17334e9-ca7c-4df9-b763-371c280399ee&properties=dealname&properties=amount&properties=dealstage&properties=dealtype&properties=num_associated_contacts&properties=closedate')
                offset = deals['offset']
                hasMore = deals['hasMore']
            for deal in deals['deals']:
                data = dict()
                data['dealID'] = deal['dealId']
                data['portal'] = deal['portalId']
                #properties = e['properties']
                costumer = dict()
                try:
                    data['name'] = deal['properties']['dealname']['value']
                except KeyError:
                    data['name'] = ''
                try:
                    data['stage'] = deal['properties']['dealstage']['value']
                except KeyError:
                    data['stage'] = ''
                try:
                    data['amount'] = deal['properties']['amount']['value']
                except KeyError:
                    data['amount'] = 0
                try:
                    data['payment'] = deal['properties']['dealtype']['value']
                    if data['payment'] == 'recurring':
                        data['isRecurring'] = True
                    if data['payment'] == 'oneoff':
                        data['isOneOff'] = True
                except KeyError:
                    data['payment'] = ''
                    data['isRecurring'] = False
                    data['isOneOff'] = False

                try:
                    dd = deal['properties']['closedate']['value']
                    date = datetime.datetime.fromtimestamp(long(dd) / 1000).strftime('%Y-%m-%d %H:%M:%S')
                    data['closedate'] = date
                except KeyError:
                    data['closedate'] = '2001-01-01 12:10:30'

                try:
                    vid = deal['associations']['associatedVids'][0]
                    costumer = self.get_contact(vid)
                except IndexError:
                    costumer = self.get_contact(vid)
                F.write(json.dumps(data) + os.linesep)
                data['isDeleted'] = False

                #database
                doc = json.dumps({'deal': data,'customer': costumer})
                self.insert_deal_n_costumer('deals', 'deals', data['dealID'], doc)
                print doc
                i += 1
        print 'Total', i
        F.close()

    def insert_deal_n_costumer(self, index, doc_type, id, body):
        self.es.create(index, doc_type,id, body)

if __name__ == "__main__":
    h = api_hub()
    h.get_all_pipelines()