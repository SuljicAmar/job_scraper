from flask import jsonify
from .services.jobs import load_jobs_for_client


def register_routes(app):
    @app.route("/jobs")
    def get_jobs():
        return load_jobs_for_client()
