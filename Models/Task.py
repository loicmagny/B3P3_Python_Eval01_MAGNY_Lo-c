from asyncio.windows_events import NULL
import datetime
from json import dump
import string
import time
from flask import Flask, json, jsonify
app = Flask(__name__)

class Task():
    def __init__(self, name, date, priority, comment):
        self.name = name;
        self.date = date;
        self.priority = priority;
        self.comment = comment;
        
def add_task(task, redis):
    try:
        if checkDate(task.date):
            if checkPriority(task.priority):
                if redis.xadd('PythonEval', task):
                    print("Task added successfully:", task)
                    return True
                else:
                    print("Error adding task to Redis stream.")
                    time.sleep(60)
        else:
            raise ValueError("Invalid date or priority for the task.")
    except ConnectionError as e:
        print("ERROR REDIS CONNECTION")
        raise e
    except Exception as e:
        print("Failed to add task")
    
    
def get_tasks(redis):
    try:
        keys = list(redis.xrange("PythonEval", 0, -1))
        return jsonify(keys)
    except Exception as e:
        raise ValueError("Impossible de récupérer les données: {}".format(str(e)))
    
def get_single_task(task, redis):
    try:
        cursor, keys = redis.scan(match=task.name)
        matching_keys = [key.decode() for key in keys]
        return [jsonify(matching_keys), True]
    except:
        raise ValueError("Impossible de récupérer les données.")
    
def remove_task(task, redis):
    try:
        toDelete = get_single_task(task, redis)
        for key in toDelete:
            redis.delete(key)
    except:
        raise ValueError("Impossible de supprimer la donnée")
    
def checkDate(date):
    if date:
        try:
            dt = datetime.datetime.strptime(date, '%Y-%m-%d')
            return True
        except ValueError:
            raise ValueError("Incorrect data format, should be YYYY-MM-DD. You gave" + date)
    else:
        raise ValueError("Incorrect data format, should be YYYY-MM-DD. You gave" + date) 

def checkPriority(priority):
    print(priority)
    if priority:
        if isinstance(priority, int):
            if priority > 2:
                raise ValueError("Priority must be between 0 and 2. You gave " + str(priority))
            elif priority < 0:
                raise ValueError("Priority must be between 0 and 2. You gave " + str(priority))
            else:
                return True
        else:
            raise ValueError("Priority must be an integer")
    else:
        return None
