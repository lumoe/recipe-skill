from src.graph_api import query_graph
import json

from flask import Flask, request
app = Flask(__name__)

@app.route('/', methods=['POST'])
def mycroft_webhook():
    return query_graph(request.get_json()) 

if __name__ == '__main__':
    app.run(debug=True, use_reloader=True)