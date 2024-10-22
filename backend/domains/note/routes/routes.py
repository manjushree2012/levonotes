from flask import Blueprint, request, jsonify

from domains.note.repo.repository.noteRepository import create_note, get_all_notes, update_note, search_notes, create_reminder, update_reminder, get_reminder_from_note, get_note, delete_note
from marshmallow import Schema, fields, ValidationError

# Create a Blueprint for the note routes
note_bp = Blueprint('notes', __name__)

# Define a schema for validation
class NoteSchema(Schema):
    title = fields.String(required=True, validate=lambda x: len(x) > 0)
    content = fields.String(required=True)

note_schema = NoteSchema()

@note_bp.route('/note', methods=['POST'])
def create_notes():
    try:
        data = note_schema.load(request.get_json())
    except ValidationError as err:
        return jsonify(err.messages), 400

    new_note = create_note(data)
    return jsonify(new_note), 201

@note_bp.route('/note/<int:note_id>', methods=['DELETE'])
def delete_notes(note_id):
    try:
        result = delete_note(note_id)
        if result:
            return jsonify({"message": f"Note with id {note_id} deleted successfully."}), 200
        else:
            return jsonify({"error": f"Note with id {note_id} not found."}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@note_bp.route('/notes', methods=['GET'])
def list_notes():
    try:
        notes = get_all_notes()
        return jsonify(notes), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@note_bp.route('/note/<int:note_id>', methods=['PUT'])
def update_notes(note_id):
    try:
        data = note_schema.load(request.get_json())
        updated_note = update_note(note_id, data)
        if updated_note:
            return jsonify(updated_note), 200
        else:
            return jsonify({"error": f"Note with id {note_id} not found."}), 404
    except ValidationError as err:
        return jsonify(err.messages), 400
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@note_bp.route('/notes/search', methods=['GET'])
def search_notes_route():
    query = request.args.get('query', '')
    if not query:
        return jsonify({"error": "Query parameter is required."}), 400

    try:
        results = search_notes(query)
        return jsonify(results), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@note_bp.route('/reminder/<int:note_id>', methods=['PUT'])
def create_or_update_reminder(note_id):
    try:
        data = request.get_json()  # Get the JSON data from the request

        # Check if a reminder with the given note_id exists
        existing_reminder = get_reminder_from_note(note_id)

        if existing_reminder:
            # Update the existing reminder with the new details
            updated_reminder = update_reminder(existing_reminder['id'], data)
            return jsonify(updated_reminder), 200
        else:
            note_exists = get_note(note_id)

            if note_exists:
                data['note_id'] = note_id  # Ensure the note_id is included in the data
                new_reminder = create_reminder(data)
                return jsonify(new_reminder), 201
            else:
                return jsonify({"error": f"Note with id {note_id} not found."}), 404
    except ValidationError as err:
        return jsonify(err.messages), 400
    except Exception as e:
        return jsonify({"error": str(e)}), 500