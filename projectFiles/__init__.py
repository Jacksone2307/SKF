from os import environ as env
from authlib.integrations.flask_client import OAuth
from dotenv import find_dotenv, load_dotenv
from urllib.parse import quote_plus, urlencode
from flask import Flask, request, session, render_template, redirect, url_for
from pathlib import Path
from requests import post
import base64
import json
from sqlalchemy import create_engine, inspect
from sqlalchemy.orm import sessionmaker, clear_mappers
from sqlalchemy.pool import NullPool
import projectFiles.adapters.repository as repo

"""Initialise our Flask application"""


oauth = None

def get_token(client_id, client_secret):
    """Obtain an access token from Spotify."""

    auth_string = client_id + ':' + client_secret
    auth_bytes = auth_string.encode('utf-8')
    auth_base64 = str(base64.b64encode(auth_bytes), "utf-8")

    url = "https://accounts.spotify.com/api/token"
    headers = {
        "Authorization": "Basic " + auth_base64,
        "Content-Type": "application/x-www-form-urlencoded" 
    }
    data = {"grant_type": "client_credentials"}
    r = post(url, headers=headers, data=data)
    json_result = json.loads(r.content)
    token = json_result["access_token"]
    return token

def instantiate_app():
    #Load environment variables
    ENV_FILE = find_dotenv()
    if ENV_FILE:
        load_dotenv(ENV_FILE)

    app = Flask(__name__)
    app.config.from_object("config.Config")

    #Setup OAuth
    oauth = OAuth(app)
    oauth.register(
        "auth0",
        client_id=env.get("AUTH0_CLIENT_ID"),
        client_secret=env.get("AUTH0_CLIENT_SECRET"),
        client_kwargs={
            "scope": "openid profile email",
        },
        server_metadata_url=f'https://{env.get("AUTH0_DOMAIN")}/.well-known/openid-configuration',
    )
    
    #Setup Database
    db_uri = app.config['DB_URI']
    db_echo = app.config['DB_ECHO']
    db_engine = create_engine(db_uri, connect_args={"check_same_thread": False}, echo=db_echo, poolclass=NullPool)
    session_fact = sessionmaker(autocommit=False, autoflush=True, bind=db_engine)
    repo.repo_instance = SqlAlchemyRepository(session_fact)



    #Setup routes
    @app.route("/callback", methods=["GET", "POST"])
    def callback():
        token = oauth.auth0.authorize_access_token()
        session["user"] = token
        return redirect(url_for("home_bp.home"))


    @app.route("/login")
    def login():
        return oauth.auth0.authorize_redirect(
            redirect_uri=url_for("callback", _external=True)
        )


    @app.route("/logout")
    def logout():
        session.clear()
        return redirect(
            "https://"
            + env.get("AUTH0_DOMAIN")
            + "/v2/logout?"
            + urlencode(
                {
                    "returnTo": url_for("home_bp.home", _external=True),
                    "client_id": env.get("AUTH0_CLIENT_ID"),
                },
                quote_via=quote_plus,
            )
        )

    with app.app_context():
        from .home import home
        app.register_blueprint(home.home_blueprint)

        from .authentication import authentication
        app.register_blueprint(authentication.authentication_blueprint)

    return app
