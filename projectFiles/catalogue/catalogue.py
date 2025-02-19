from flask import Blueprint, render_template, session, request, jsonify, make_response
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, BooleanField
from projectFiles.domainmodel.model import *
from .catalogue_service import get_tracks, search_tracks
from ..playlists.playlists_service import get_playlists

catalogue_blueprint = Blueprint('catalogue_bp', __name__)

@catalogue_blueprint.route('/catalogue', methods=['GET', 'POST'])
def catalogue():
    search_form = CatalogueSearchForm()
    tracks = get_tracks()
    playlists = None
    if "user" in session:
        playlists = get_playlists(session["user"]["userinfo"]["email"])
    if search_form.validate_on_submit():
        print(f"Searching for {search_form.search_field.data}....")
        tracks = search_tracks(search_form.search_field.data)
       
    return render_template('catalogue/catalogue.html', tracks=tracks, search_form=search_form, playlists=playlists)

class CatalogueSearchForm(FlaskForm):
    search_field  = StringField("Song Name: ", render_kw={"placeholder" : "Song Name..."})
    search_button = SubmitField('Search')

class CatalogueAddForm(FlaskForm):
    title_field = StringField("Song Title: ", render_kw={"placeholder": "Song Name..."})
    ###HERE
    # url_field = StringField("")
    
    
