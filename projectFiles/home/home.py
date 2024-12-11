from .home_service import induce_search
from flask import Blueprint, render_template
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField



home_blueprint = Blueprint('home_bp', __name__)

@home_blueprint.route('/', methods=['GET', 'POST'])
def home():
    search_form = SearchForm()
    key = ""
    url = None

    if search_form.validate_on_submit():
        try:
            key, url = induce_search(search_form.search_field.data)
        except:
            key = ""
            url = None

    print(f"key: {key}")
    return render_template('home/home.html', search_form=search_form, key=key, url=url)



class SearchForm(FlaskForm):
    search_field = StringField("Song name: ", render_kw={"placeholder" : "Song Name..."})
    search_button = SubmitField('Search')