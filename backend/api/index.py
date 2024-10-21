from flask import Flask, request, jsonify
from .repo import create_note, delete_note, get_all_notes, update_note
from flask_cors import CORS

from marshmallow import Schema, fields, ValidationError

app = Flask(__name__)

# Enable CORS for all routes
CORS(app)

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

@app.route('/note/<int:note_id>', methods=['DELETE'])
def delete_notes(note_id):
    try:
        result = delete_note(note_id)
        if result:
            return jsonify({"message": f"Note with id {note_id} deleted successfully"}), 200
        else:
            return jsonify({"error": f"Note with id {note_id} not found"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/notes', methods=['GET'])
def list_notes():
    try:
        notes = get_all_notes()
        return jsonify(notes), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/note/<int:note_id>', methods=['PUT'])
def update_notes(note_id):
    try:
        data = note_schema.load(request.get_json())
        updated_note = update_note(note_id, data)
        if updated_note:
            return jsonify(updated_note), 200
        else:
            return jsonify({"error": f"Note with id {note_id} not found"}), 404
    except ValidationError as err:
        return jsonify(err.messages), 400
    except Exception as e:
        return jsonify({"error": str(e)}), 500