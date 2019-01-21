from adapt.intent import IntentBuilder
from mycroft import intent_file_handler
from mycroft.skills.core import MycroftSkill
from mycroft.util.log import getLogger
import requests
import json 
import os
import random

LOGGER = getLogger(__name__)

BASE_DIR = os.path.dirname(os.path.abspath( __file__ ))

class RecipeSkill(MycroftSkill):
    def __init__(self):
        super(RecipeSkill, self).__init__(name="RecipeSkill")

    @intent_file_handler('recipe.intent')
    def handle_recipe_with_ingredients(self, message):
        if message.data.get('ingredient', None) == None:
            self.speak_dialog("recipes.no.ingredient")
            return 
        r = json.loads(
            query_graph(
                    {
                        "ingredient": explode_multiple_ingredients(message.data['ingredient'])
                    })
            )
        index = random.randint(0, len(r['results']['bindings']))
        first_recipe =  r['results']['bindings'][index]['name']['value']
        total_time =  r['results']['bindings'][index]['totalTime']['value'].replace('PT','').replace('M', '')
        # If total time is 75 the recipe takes longe than 60 minutes 
        if total_time == '75':
            total_time = 'at least 60'
        
        self.speak_dialog("recipes.with.ingredients", data={"recipe": first_recipe, "total_time": total_time})
    
    @intent_file_handler('recipe.time.low.intent')
    def handle_recipe_with_ingredients_time_low(self, message):
        if message.data.get('ingredient', None) == None:
            self.speak_dialog("recipes.no.ingredient")
            return 
        r = json.loads(
            query_graph(
                    {
                        "ingredient": explode_multiple_ingredients(message.data['ingredient'])
                    })
            )
        fastest_recipe_index = get_recipe_with_lowest_cooking_time(r)
        first_recipe =  r['results']['bindings'][fastest_recipe_index]['name']['value']
        total_time =  r['results']['bindings'][fastest_recipe_index]['totalTime']['value'].replace('PT','').replace('M', '')
        # If total time is 75 the recipe takes longe than 60 minutes 
        if total_time == '75':
            total_time = 'at least 60'

        self.speak_dialog("recipes.with.ingredients.time.low", data={"recipe": first_recipe, "total_time": total_time})


def explode_multiple_ingredients(ingredients):
    ingredients = ingredients.replace('and', '').strip()
    return ingredients.split()

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

def get_recipe_with_lowest_cooking_time(recipes):
    times = list(map(lambda x: x['totalTime']['value'].replace('PT','').replace('M', ''), recipes['results']['bindings']))
    lowest_time_index = 0
    for i, time in enumerate(times): 
        if time < times[lowest_time_index]:
            lowest_time_index = i
    
    return lowest_time_index

if __name__ == '__main__':
    get_recipe_with_lowest_cooking_time('')
