#!flask/bin/python
from flask import Flask, jsonify
from flask import abort
from flask import make_response


app = Flask(__name__)


@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)


# ####### #
# Profile #
# ####### #

@app.route('/todo/api/v1.0/tasks/<int:task_id>', methods=['GET'])
def get_task(task_id):
    task = [task for task in tasks if task['id'] == task_id]
    if len(task) == 0:
        abort(404)
    return jsonify({'task': task[0]})


# ####### #
# Profile #
# ####### #


if __name__ == '__main__':
    app.run(debug=True)
