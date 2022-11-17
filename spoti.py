import os
import requests
import flask
from flask import send_file
# from flask import render_template
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired

from modules.spotmodule import dl


app = flask.Flask(__name__)
app.config['SECRET_KEY'] = 'secret_pass'

class UrlForm(FlaskForm):
    spoturl = StringField('Spotify URL', validators=[DataRequired()])
    submit = SubmitField('Download')

@app.route('/', methods=['GET', 'POST'])
def index():
    form = UrlForm()
    if form.validate_on_submit():
        dl(form.spoturl.data)
        return '<h1>' + form.spoturl.data + '</h1>' + '<a href="" download> song </a>'

    return flask.render_template('index.html', form = form)

@app.route('/download')
def download():
    path = ''
    return send_file(path, as_attachment=True)

#     """

#     """

#     return flask.render_template(
#         'index.html',

#         )

app.run(debug=True)
