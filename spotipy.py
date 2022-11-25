import logging
import os.path
import os
from dotenv import load_dotenv
load_dotenv()
import flask
from flask_sqlalchemy import SQLAlchemy
from flask import Flask, render_template, request, redirect, url_for, flash, send_from_directory
from werkzeug.utils import secure_filename
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo
from werkzeug.utils import secure_filename
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin, LoginManager, current_user, login_user, logout_user, login_required
from modules.spotmodule import dl

# [logging config
logging.basicConfig(format='%(asctime)s:%(levelname)s:%(filename)s:%(funcName)s:%(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S',
                    level=logging.INFO)
# logging config]


app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DATABASE_URL")
db = SQLAlchemy(app)
# user_loader must be in the same place login manager is instantiated
# https://stackoverflow.com/a/44776737
login = LoginManager(app)
@login.user_loader
def load_user(id):
    return Person.query.get(int(id))
login.login_view = 'login'
app.secret_key = "secretpass"
app.config['ALLOWED_EXTENSIONS'] = ['.mp3', '.m4a']
app.config['MAX_CONTENT_LENGTH'] = 20 * 1024 * 1024 # 20mb

# create music folder if it does not exist in app root dir
MUSIC_FOLDER = 'music'
if not os.path.exists(MUSIC_FOLDER):
    os.makedirs(MUSIC_FOLDER, exist_ok=True)
    
# folder to temp download and zip spoturl songs
SPOTURL_FOLDER = 'spotify'
if not os.path.exists('spotify'):
    os.makedirs('spotify', exist_ok=True)

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
        # flash("Download in progress. Please wait")
        dl(form.spoturl.data)
        flash('Music succesfully downloaded to library. \
            spotify.zip contains all files from requested Spotify URL')
        # redirect(url_for('music'))
    return render_template('index.html', form = form)

@app.route('/upload', methods=['GET'])
@login_required
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
            flash('Not allowed file type. \
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


@app.route('/music', methods=['GET'])
def list_files():
    """Endpoint to list files."""
    logging.info('Listing files stored in the music folder.')
    music_files = []
    for filename in os.listdir(MUSIC_FOLDER):
        # only append mp3 or m4a files to music_list
        if '.m4a' in filename or '.mp3' in filename or '.zip' in filename:
            path = os.path.join(MUSIC_FOLDER, filename)
            if os.path.isfile(path):
                music_files.append(filename)

    return render_template('music.html', files=music_files)


class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = Person.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        return redirect(url_for('index'))
    return render_template('login.html', title='Sign In', form=form)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))

class Person(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128))
    song = db.relationship('Song', backref='listeners', lazy='dynamic')
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self) -> str:
        return f"Person with username: {self.username} and email: {self.email}"

class Song(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    song_name = db.Column(db.String(80), index=True)
    artist = db.Column(db.String(80), index=True)
    playlist = db.Column(db.String(80))
    user_id = db.Column(db.Integer, db.ForeignKey('person.id'))
    
    def __repr__(self):
        return f"{self.song_name}"

class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    password2 = PasswordField(
        'Repeat Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Register')

    def validate_username(self, username):
        user = Person.query.filter_by(username=username.data).first()
        if user is not None:
            raise ValidationError('Please use a different username.')

    def validate_email(self, email):
        user = Person.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError('Please use a different email address.')

    @app.route('/register', methods=['GET', 'POST'])
    def register():
        if current_user.is_authenticated:
            return redirect(url_for('index'))
        form = RegistrationForm()
        if form.validate_on_submit():
            user = Person(username=form.username.data, email=form.email.data)
            user.set_password(form.password.data)
            db.session.add(user)
            db.session.commit()
            flash('Congratulations, you are now a registered user!')
            return redirect(url_for('login'))
        return render_template('register.html', title='Register', form=form)



with app.app_context():
    db.create_all()


# app.run(debug=False)
