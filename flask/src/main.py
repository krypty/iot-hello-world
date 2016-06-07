#!usr/bin/python3
# coding: utf-8
from flask import Flask, jsonify, abort, request, make_response, url_for
import MySQLdb as mdb

app = Flask(__name__, static_url_path="")

MYSQL_USERNAME = "toto"
MYSQL_PASSWORD = "password"
MYSQL_HOST = "mysqlsrv"
MYSQL_DB = "todo_list"
TASKS_TABLE = "tbl_tasks"

# MySQL configurations

con = mdb.connect(MYSQL_HOST, MYSQL_USERNAME, MYSQL_PASSWORD, MYSQL_DB)


@app.errorhandler(400)
def bad_request(error):
    return make_response(jsonify({'error': 'Bad request'}), 400)


@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)

tasks = [
    {
        'id': 1,
        'title': u'Buy groceries',
        'description': u'Milk, Cheese, Pizza, Fruit, Tylenol',
        'done': False
    },
    {
        'id': 2,
        'title': u'Learn Python',
        'description': u'Need to find a good Python tutorial on the web',
        'done': False
    }
]


def make_public_task(task):
    new_task = {}

    new_task["id"] = task[0]
    new_task["title"] = task[1]
    new_task["description"] = task[2]
    new_task["done"] = True if task[3] == 1 else False
    new_task['uri'] = url_for('get_task', task_id=task[0], _external=True)

    return new_task


@app.route('/todo/api/v1.0/tasks', methods=['GET'])
def get_tasks():
    with con:
        cur = con.cursor()
        sql = """SELECT * FROM %s""" % TASKS_TABLE
        cur.execute(sql)

        results = cur.fetchall()

        return jsonify({'tasks': [make_public_task(task) for task in results]})

    abort(400)


@app.route('/todo/api/v1.0/tasks/<int:task_id>', methods=['GET'])
def get_task(task_id):
    with con:
        cur = con.cursor()
        sql = """SELECT * FROM %s WHERE id=%s""" % (TASKS_TABLE, task_id)
        cur.execute(sql)

        results = cur.fetchall()

        if len(results) == 0:
            abort(404)

        task = results[0]
        return jsonify({'task': make_public_task(task)})

    abort(400)


@app.route('/todo/api/v1.0/tasks', methods=['POST'])
def create_task():
    if not request.json or not 'title' in request.json:
        abort(400)
    task = {
        'id': tasks[-1]['id'] + 1,
        'title': request.json['title'],
        'description': request.json.get('description', ),
        'done': False
    }
    tasks.append(task)
    return jsonify({'task': make_public_task(task)}), 201


@app.route('/todo/api/v1.0/tasks/<int:task_id>', methods=['PUT'])
def update_task(task_id):
    task = list(filter(lambda t: t['id'] == task_id, tasks))
    if len(task) == 0:
        abort(404)
    if not request.json:
        abort(400)
    if 'title' not in request.json:
        abort(400)
    if 'description' not in request.json:
        abort(400)
    if 'done' in request.json and not isinstance(request.json['done'], bool):
        abort(400)
    task[0]['title'] = request.json.get('title', task[0]['title'])
    task[0]['description'] = request.json.get(
        'description', task[0]['description'])
    task[0]['done'] = request.json.get('done', task[0]['done'])
    return jsonify({'task': make_public_task(task[0])})


@app.route('/todo/api/v1.0/tasks/<int:task_id>', methods=['DELETE'])
def delete_task(task_id):
    task = list(filter(lambda t: t['id'] == task_id, tasks))
    if len(task) == 0:
        abort(404)
    tasks.remove(task[0])
    return jsonify({'result': True})


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug=True)
