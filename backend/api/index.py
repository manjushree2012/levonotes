from flask import Flask, request
from repo import create_note

app = Flask(__name__)

@app.route('/')
def home():
    return 'Hello, World!'

@app.route('/about')
def about():
    return 'About'

@app.route('/note', methods=['POST'])
def create_notes():
    data = request.get_json()

    create_note(data)

    return [1,2,3]