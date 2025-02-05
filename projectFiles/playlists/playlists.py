from flask import Blueprint, render_template, session, request, jsonify, make_response
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, BooleanField
from projectFiles.domainmodel.model import *
from .playlists_service import create_playlist, get_playlists, search_playlists

playlists_blueprint = Blueprint('playlists_bp', __name__)

@playlists_blueprint.route('/playlists', methods=['GET', 'POST'])
def playlists():
    create_form = PlaylistCreateForm()
    search_form = PlaylistSearchForm()
    if create_form.validate_on_submit():
        create_playlist(create_form.name_field.data)
    playlists = get_playlists(session["user"]["userinfo"]["email"])
    
    if search_form.validate_on_submit():
        playlists = search_playlists(search_form.search_field.data)
    return render_template('playlists/playlists.html', search_form = search_form, create_form = create_form, playlists=playlists)
    

class PlaylistSearchForm(FlaskForm):
    search_field  = StringField("Playlist Name: ", render_kw={"placeholder" : "Playlist Name..."})
    search_button = SubmitField('Search')

class PlaylistCreateForm(FlaskForm):
    name_field = StringField("Playlist Name: ", render_kw={"placeholder": "Playlist Name..."})
    create_button = SubmitField('Create')
