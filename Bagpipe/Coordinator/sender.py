"""
=====
sender.py
=====

Import data from server.

============================

"""
from flask import Flask, jsonify
from flask import make_response
from config import sender_links


app = Flask(__name__)


@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)


# ####### #
# Profile #
# ####### #

@app.route(sender_links['user'], methods=['GET'])
def get_users(task_id):
    task = [task for task in tasks if task['id'] == task_id]
    if len(task) == 0:
        abort(404)
    return jsonify({'task': task[0]})


def get_products(task_ids):
    pass


# ####### #
# Profile #
# ####### #