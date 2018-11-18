import requests
import json 

def make_query():
    URI = 'http://graphdb.sti2.at:8080/repositories/broker-graph'
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'X-Requested-With': 'XMLHttpRequest',
        'Accept': 'application/sparql-results+json,*/*;q=0.9'
    }
    data = {
        'query': construct_query()
    }

    response = requests.post(URI, data=data, headers=headers)
    r = json.loads(response.text)
    for recipe in r['results']['bindings']:
        print(recipe['name']['value'])

def construct_query(data=''):
    with open('query.rq', 'r') as query:
        return query.read()

if __name__ == '__main__':
    make_query()