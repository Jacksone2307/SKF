from flask import Flask, request, session, render_template
from pathlib import Path

"""Initialise our Flask application"""

def instantiate_app():
    app = Flask(__name__)
    app.config.from_object("config.Config")

    with app.app_context():
        from .home import home
        app.register_blueprint(home.home_blueprint)

    return app
