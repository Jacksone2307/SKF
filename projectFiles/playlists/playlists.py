from flask import Blueprint, render_template, session, request, jsonify, make_response
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, BooleanField
from projectFiles.domainmodel.model import *


playlists_blueprint = Blueprint('playlists_bp', __name__)

@playlists_blueprint.route('/playlists', methods=['GET', 'POST'])
def playlists():


    return render_template('playlists/playlists.html')
    
    
