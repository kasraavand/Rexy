#!flask/bin/python
import sys
sys.path.append('/home/tci/Recommender_System')

from flask import Flask, jsonify
from flask import abort
from flask import request
from configuration import config
import json

app = Flask(__name__)


@app.route(config.receive_links['users'], methods=['POST'])
def get_users():
    results = request.json
    if not results:
        abort(400)
    with open("users.json", 'a+') as f:
        json.dump(results, f, indent=4)
    return jsonify("{'status': True}")


@app.route(config.receive_links['products'], methods=['POST'])
def get_products():
    results = request.json
    if not results:
        abort(400)
    with open("products.json", 'a+') as f:
        json.dump(results, f, indent=4)
    return jsonify("{'status': True}")


if __name__ == '__main__':
    app.run(debug=True, port=80)
