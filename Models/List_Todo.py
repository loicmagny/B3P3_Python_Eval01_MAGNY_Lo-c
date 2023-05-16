from flask import Flask, jsonify
app = Flask(__name__)

class List_ToDo():
    def __init__(self, name, date, priority, comment):
        self.name = name;
        