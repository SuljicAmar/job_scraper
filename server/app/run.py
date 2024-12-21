from flask import Flask
from flask_cors import CORS
from .routes import register_routes  # Import a function to register routes

app = Flask(__name__)
CORS(app)
register_routes(app)  # Pass the app object to register routes

if __name__ == "__main__":
    app.run(debug=True)
