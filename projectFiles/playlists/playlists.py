from flask import Blueprint, render_template, redirect, url_for, session, request, jsonify, make_response
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, BooleanField
from projectFiles.domainmodel.model import *
from .playlists_service import create_playlist, get_playlists, search_playlists, get_track, add_to_playlist, search_tracks
import projectFiles.adapters.repository as repo


playlists_blueprint = Blueprint('playlists_bp', __name__)
repo_instance : repo.AbstractRepository = repo.repo_instance

@playlists_blueprint.route('/playlists', methods=['GET', 'POST'])
def playlists():
    if "user" not in session:
        return redirect("/login")
    
    
    # playlist = repo_instance.search_playlists(session["user"]["userinfo"]["email"], "YES")[0]
    # track = repo_instance.get_track(1)
    # print(playlist)
    # print(track)
    # playlist.add_track(track)
    # print(playlist)

    create_form = PlaylistCreateForm()
    search_form = PlaylistSearchForm()

    if create_form.validate_on_submit() and create_form.name_field.data is not None:
        create_playlist(create_form.name_field.data)
    playlists = get_playlists(session["user"]["userinfo"]["email"])
    
    if search_form.validate_on_submit():
        playlists = search_playlists(search_form.search_field.data)
    return render_template('playlists/playlists.html', search_form = search_form, create_form = create_form, playlists=playlists)

@playlists_blueprint.route('/playlist/<playlist>', methods=['GET', 'POST'])
def playlist(playlist: str):
    # try:
    target_playlist = search_playlists(playlist)[0]
    tracks = target_playlist.tracks
    search_form = CatalogueSearchForm()
    if search_form.validate_on_submit():
        print(f"Searching for {search_form.search_field.data}....")
        tracks = search_tracks(playlist, search_form.search_field.data)
    playlists = get_playlists(session["user"]["userinfo"]["email"])
    return render_template('playlists/playlist.html', search_form = search_form, tracks = tracks, playlist = playlist, playlists=playlists)
    # except:
    #     return redirect('/')



@playlists_blueprint.route('/add_track', methods=['POST'])
def add_track():
    r = request.get_json()
    playlist_title = r["playlist_title"]
    track_id = r["track_id"]
    playlist = search_playlists(playlist_title)[0]  ###Add the same get method for playlists as have done with tracks.
    track = get_track(track_id)
    
    add_to_playlist(playlist, track)

    response = make_response(jsonify({"message": "JSON received"}), 200)
    return response
class PlaylistSearchForm(FlaskForm):
    search_field  = StringField("Playlist Name: ", render_kw={"placeholder" : "Playlist Name..."})
    search_button = SubmitField('Search')

class PlaylistCreateForm(FlaskForm):
    name_field = StringField("Playlist Name: ", render_kw={"placeholder": "Playlist Name..."})
    create_button = SubmitField('Create')

class CatalogueSearchForm(FlaskForm):
    search_field  = StringField("Song Name: ", render_kw={"placeholder" : "Song Name..."})
    search_button = SubmitField('Search')
