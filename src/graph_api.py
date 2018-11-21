import requests
import json 
import os

def execute_query(input_data):
    URI = 'http://graphdb.sti2.at:8080/repositories/broker-graph'
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'X-Requested-With': 'XMLHttpRequest',
        'Accept': 'application/sparql-results+json,*/*;q=0.9'
    }
    data = {
        'query': construct_query(input_data)
    }

    # print(data.get('query'))
    response = requests.post(URI, data=data, headers=headers)
    r = json.loads(response.text)
    # for recipe in r['results']['bindings']:
    #    print(recipe['name']['value'])

    return response.text

def construct_query(data):
    with open(os.path.join('src', 'query.rq'), 'r') as query_file:
        query = query_file.read()
        query = query.replace('{ingredients}', "  && ".join(data.get('ingredients')))
 
        return query

def query_graph(data):
    return execute_query(data)

if __name__ == '__main__':
    execute_query({
            "ingredients": [
        "Eier", 
        "Zwiebel"
    ]
        })