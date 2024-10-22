from flask import Flask
from flask_cors import CORS
from domains.note.routes.routes import note_bp

app = Flask(__name__)

# Enable CORS for all routes
CORS(app)

# Register the note routes Blueprint
app.register_blueprint(note_bp)

if __name__ == '__main__':
    app.run(debug=True)
   