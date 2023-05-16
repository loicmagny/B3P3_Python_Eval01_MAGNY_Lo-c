import redis
from flask import Flask, jsonify
from Models.List_Todo import List_ToDo
from Models.Task import Task, add_task
from Models.Task import get_tasks

app = Flask(__name__)

r = redis.Redis(host='localhost', port=5000, db=1)

@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"


@app.route('/list/create')
def handle_create_list():
    list = List_ToDo('test')
    redis.xadd('PythonEval', list)
    
    
@app.route('/list/')
def handle_get_all_lists():
    keys = list(r.xrange("PythonEval", 0, -1))
    return jsonify(keys)
    

@app.route('/list/<name>')
def handle_get_list(name):
    try:
        cursor, keys = redis.scan(match=name)
        matching_keys = [key.decode() for key in keys]
        return [jsonify(matching_keys), True]
    except:
        raise ValueError("Impossible de récupérer les données.")

# @app.route('/list/update/<name>')
# def handle_list_update(name):
#     try:
#         cursor, keys = redis.scan(match=name)
#         matching_keys = [key.decode() for key in keys]
#         return [jsonify(matching_keys), True]
#     except:
    
#         raise ValueError("Impossible de récupérer les données.")

@app.route('/list/delete/<name>')
def handle_list_remove(name):
    try:
        cursor, keys = redis.scan(match=name)
        matching_keys = [key.decode() for key in keys]
        for key in matching_keys:
            redis.delete(key)
    except:
    
        raise ValueError("Impossible de récupérer les données.")

@app.route('/task/add', methods=['GET'])
def handle_create_task():
    try:
        task = Task('Test', '2023-06-16', 0, '')
        success = add_task(task, r)
        if success:
            return 'Task created successfully', 200
        else:
            return 'Failed to create task', 500
    except ValueError:
        raise ValueError("La tâche n'a pas pu être créée")
    
@app.route('/task/', methods=['GET'])
def handle_get_all():
    try:
        tasks = get_tasks(r)
        if tasks[1]:
            return tasks[0]
        else:
            return 'Failed to get tasks'
    except ValueError:
        raise ValueError("Les tâches n'ont pas pu être récupérées")
    
    
    
@app.route('/task/remove', methods=['GET'])
def handle_remove_task():
    return True
    
    
if __name__ == '__main__':
    app.run()
