from adapt.intent import IntentBuilder
from mycroft import intent_file_handler
from mycroft.skills.core import MycroftSkill
from mycroft.util.log import getLogger
import requests
import json 
import os


LOGGER = getLogger(__name__)

BASE_DIR = os.path.dirname(os.path.abspath( __file__ ))

class RecipeSkill(MycroftSkill):
    def __init__(self):
        super(RecipeSkill, self).__init__(name="RecipeSkill")

    @intent_file_handler('recipe.intent')
    def handle_recipe_with_ingredients(self, message):
        r = json.loads(query_graph({"ingredient": [message.data['ingredient']]}))
        first_recipe =  r['results']['bindings'][0]['name']['value']
        total_time =  r['results']['bindings'][0]['totalTime']['value'].replace('PT','').replace('M', '')
        
        self.speak_dialog("recipes.with.ingredients", data={"recipe": first_recipe, "total_time": total_time})

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

    response = requests.post(URI, data=data, headers=headers)
    r = json.loads(response.text)

    return response.text

def construct_query(data):
    with open(os.path.join(BASE_DIR, 'query.rq'), 'r') as query_file:
        query = query_file.read()
        query = query.replace('{ingredients}', "  && ".join(data.get('ingredient')))
 
        return query

def query_graph(data):
    return execute_query(data)

def create_skill():
    return RecipeSkill()
