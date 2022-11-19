import logging
import os.path
import os
import sys

from flask import Flask, render_template, request, redirect, url_for, flash, send_from_directory
from werkzeug.utils import secure_filename
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired
from werkzeug.utils import secure_filename

from modules.spotmodule import dl

# [logging config
logging.basicConfig(format='%(asctime)s:%(levelname)s:%(filename)s:%(funcName)s:%(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S',
                    level=logging.INFO)
# logging config]


app = Flask(__name__)
app.secret_key = "secretpass"

app.config['ALLOWED_EXTENSIONS'] = ['.mp3', '.m4a']
app.config['MAX_CONTENT_LENGTH'] = 20 * 1024 * 1024 # 20mb

# create music folder if it does not exist in app root dir
MUSIC_FOLDER = 'music'
if not os.path.exists(MUSIC_FOLDER):
    os.makedirs(MUSIC_FOLDER, exist_ok=True)

MUSIC_FOLDER =  os.path.join(os.getcwd(), MUSIC_FOLDER)

class UrlForm(FlaskForm):
    spoturl = StringField('Spotify URL', validators=[DataRequired()])
    submit = SubmitField('Download')

# http://localhost:5000
@app.route('/', methods=['GET', 'POST'])
def index():
    logging.info('Showing index page')
    form = UrlForm()
    if form.validate_on_submit():
        dl(form.spoturl.data)
        flash('Download Successful')
        # redirect(url_for('music'))
    return render_template('index.html', form = form)

@app.route('/upload', methods=['GET'])
def upload():
    logging.info('Showing index page')
    return render_template('upload.html')

@app.route('/upload', methods=['POST'])
def music_files():
    """Upload a file."""
    logging.info('Starting file upload')

    if 'file' not in request.files:
        flash('No file part')
        return render_template('upload.html')

    file = request.files['file']
    # obtaining the name of the destination file
    filename = file.filename
    if filename == '':
        logging.info('Invalid file.')
        flash('No file selected for uploading')
        return redirect(request.url)
    else:
        logging.info('Selected file is= [%s]', filename)
        file_ext = os.path.splitext(filename)[1]
        if file_ext in app.config['ALLOWED_EXTENSIONS']:
            secure_fname = secure_filename(filename)
            file.save(os.path.join(MUSIC_FOLDER, secure_fname))
            logging.info('Upload is successful')
            flash('File uploaded successfully')
            return redirect('/upload')
        else:
            logging.info('Invalid file extension.')
            flash('Not allowed file type \
                Invalid file extension. \
                \n Allowed extensions are mp3 and m4a. \
                \n Max size is 20mb')
            return redirect(request.url)


@app.route('/download/<path:filename>', methods=['GET'])
def download(filename):
    """Download a file."""
    logging.info('Downloading file= [%s]', filename)
    logging.info(app.root_path)
    full_path = os.path.join(app.root_path, MUSIC_FOLDER)
    logging.info(full_path)
    return send_from_directory(full_path, filename, as_attachment=True)


# http://localhost:5000/files
@app.route('/music', methods=['GET'])
def list_files():
    """Endpoint to list files."""
    logging.info('Listing files stored in the music folder.')
    music_files = []
    for filename in os.listdir(MUSIC_FOLDER):
        path = os.path.join(MUSIC_FOLDER, filename)
        if os.path.isfile(path):
            music_files.append(filename)

    return render_template('music.html', files=music_files)
    

app.run(debug=False)
