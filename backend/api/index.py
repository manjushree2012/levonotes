from flask import Flask, request, jsonify
from .repo import create_note

from marshmallow import Schema, fields, ValidationError

app = Flask(__name__)

@app.route('/')
def home():
    return 'Hello, World!'

@app.route('/about')
def about():
    return 'About'

# Define a schema for validation
class NoteSchema(Schema):
    title = fields.String(required=True, validate=lambda x: len(x) > 0)
    content = fields.String(required=True)

note_schema = NoteSchema()

@app.route('/note', methods=['POST'])
def create_notes():
    try:
        data = note_schema.load(request.get_json())
    except ValidationError as err:
        return jsonify(err.messages), 400

    new_note = create_note(data)
    return jsonify(new_note), 201