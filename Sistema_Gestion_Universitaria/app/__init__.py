import os
from flask import Flask, redirect, url_for, session
from config import Config
from app.db import init_db
from app.auth import auth_bp
from app.students import students_bp
from app.academic import academic_bp
from app.requests import requests_bp

def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_object(Config)
    if test_config:
        app.config.update(test_config)

    os.makedirs(app.instance_path, exist_ok=True)
    db_path = app.config["DATABASE"]
    if not os.path.isabs(db_path):
        app.config["DATABASE"] = os.path.join(app.root_path, "..", db_path)
    os.makedirs(os.path.dirname(app.config["DATABASE"]), exist_ok=True)

    init_db(app)
    app.register_blueprint(auth_bp)
    app.register_blueprint(students_bp)
    app.register_blueprint(academic_bp)
    app.register_blueprint(requests_bp)

    @app.get("/")
    def index():
        if session.get("user_id"):
            return redirect(url_for("students.list_students"))
        return redirect(url_for("auth.login"))

    return app
