#!usr/bin/python
# coding: utf-8
from flask import Flask, jsonify, abort, request, make_response, url_for
import MySQLdb as mdb
from collections import OrderedDict
import os

app = Flask(__name__, static_url_path="")

MYSQL_USERNAME = os.environ["MYSQL_USERNAME"]
MYSQL_PASSWORD = os.environ["MYSQL_PASSWORD"]
MYSQL_HOST = os.environ["MYSQL_HOSTNAME"]
MYSQL_DB = os.environ["MYSQL_DB"]
TASKS_TABLE = os.environ["TASKS_TABLE"]

# MySQL configurations

con = mdb.connect(MYSQL_HOST, MYSQL_USERNAME, MYSQL_PASSWORD, MYSQL_DB)


@app.errorhandler(400)
def bad_request(error):
    return make_response(jsonify({'error': 'Bad request'}), 400)


@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)


def bool_to_tinyint(b):
    if not isinstance(b, bool):
        raise ValueError("Value is not a bool")
    return 1 if b == True else 0


def tinyint_to_bool(ti):
    if not isinstance(ti, int):
        raise ValueError("Value is not a int")
    return False if ti == 0 else True


def make_public_task(task):
    print "make_public_task : " + str(task)
    new_task = OrderedDict()

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


def get_raw_task(task_id):
    with con:
        cur = con.cursor()
        sql = """SELECT * FROM %s WHERE id=%s""" % (TASKS_TABLE, task_id)
        cur.execute(sql)

        results = cur.fetchall()

        if len(results) == 0:
            abort(404)

        task = results[0]
        print "task id " + str(task_id) + ": " + str(task)
        return make_public_task(task)
    return None


@app.route('/todo/api/v1.0/tasks/<int:task_id>', methods=['GET'])
def get_task(task_id):
    task = get_raw_task(task_id)
    return jsonify({'task': task})

    abort(400)


@app.route('/todo/api/v1.0/tasks', methods=['POST'])
def create_task():
    if not request.json or not 'title' in request.json:
        abort(400)
    task = {
        'title': request.json['title'],
        'description': request.json['description'],
        'done': "0"
    }

    try:
        cur = con.cursor()
        sql = "INSERT INTO " + MYSQL_DB + "." + TASKS_TABLE + \
            " (title, description, done) VALUES (%s, %s, %s)"

        cur.execute(sql, (task["title"], task["description"], task["done"]))
        con.commit()
    except Exception as e:
        con.rollback()
        raise e
        abort(400)

    return get_task(cur.lastrowid), 201


@app.route('/todo/api/v1.0/tasks/<int:task_id>', methods=['PUT'])
def update_task(task_id):
    task = get_raw_task(task_id)
    print str(task)
    if task is None:
        abort(404)

    if not request.json:
        abort(400)
    if 'title' not in request.json:
        abort(400)
    if 'description' not in request.json:
        abort(400)
    if 'done' in request.json and not isinstance(request.json['done'], bool):
        abort(400)

    task['title'] = request.json.get('title', task['title'])
    task['description'] = request.json.get('description', task['description'])
    task['done'] = bool_to_tinyint(request.json.get('done', task['done']))

    try:
        cur = con.cursor()
        sql = "UPDATE " + TASKS_TABLE + " SET title=%s,description=%s,done=%s WHERE id=%s"

        cur.execute(sql, (task["title"], task[
                    "description"], task["done"], task_id))
        con.commit()
    except Exception as e:
        con.rollback()
        raise e
        abort(400)

    print str(task)
    return get_task(task_id)


@app.route('/todo/api/v1.0/tasks/<int:task_id>', methods=['DELETE'])
def delete_task(task_id):
    try:
        cur = con.cursor()
        sql = "DELETE FROM " + TASKS_TABLE + " WHERE id=%s"
        cur.execute(sql, (task_id, ))
        con.commit()

        if cur.rowcount == 1:
            return jsonify({'result': True})
        else:
            return jsonify({'result': False})
    except Exception as e:
        con.rollback()
        raise e
        abort(400)


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug=True)
