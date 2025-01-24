from .home_service import induce_search, save_track_to_db
from flask import Blueprint, render_template, session, request, jsonify, make_response
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, BooleanField
from projectFiles.domainmodel.model import *




home_blueprint = Blueprint('home_bp', __name__)

@home_blueprint.route('/', methods=['GET', 'POST'])
def home():
    search_form = SearchForm()
    key = ""
    url = None
    if search_form.validate_on_submit():
        try:
            key, url = induce_search(search_form.search_field.data, search_form.key_boolean.data)
        except:
            key = ""
            url = None
    return render_template('home/home.html', search_form=search_form, key=key, url=url)

@home_blueprint.route('/save-track', methods=['POST'])
def save_track():
    r = request.get_json()
    print(f"r = {r}")
    track = Track(r["title"], r["url"], r["key"])
    print(f"Saving {track} to db. ")
    save_track_to_db(track)
    print("Saved track to db.")
    response = make_response(jsonify({"message": "JSON received"}), 200)
    return response

class SearchForm(FlaskForm):
    search_field = StringField("Song name: ", render_kw={"placeholder" : "Song Name..."})
    search_button = SubmitField('Search')
    key_boolean = BooleanField("Get Key")