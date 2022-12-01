from zipfile import ZipFile
import zipfile
import os
import subprocess
import shutil
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
# from flask import flash

# create music folder if it does not exist in app root dir
MUSIC_FOLDER = os.path.join(os.getcwd(), 'data/music')
if not os.path.exists(MUSIC_FOLDER):
    os.makedirs(MUSIC_FOLDER, exist_ok=True)
    
# folder to temp download and zip spoturl songs
SPOTIFY_FOLDER = os.path.join(os.getcwd(), 'data/spotify')
if not os.path.exists(SPOTIFY_FOLDER):
    os.makedirs(SPOTIFY_FOLDER, exist_ok=True)

def move_files():
    source = SPOTIFY_FOLDER
    destination = MUSIC_FOLDER
 
    # gather all files
    allfiles = os.listdir(source)
 
    # iterate on all files to move them to destination folder
    for f in allfiles:
        src_path = os.path.join(source, f)
        dst_path = os.path.join(destination, f)
        shutil.move(src_path, dst_path)

def zip_dir():
    song_list = []

    # append mp3 or m4a files in specified directory to song_list
    for entry in os.scandir(SPOTIFY_FOLDER):
        if entry.is_file():
            if ('.mp3' in entry.name) or ('.m4a' in entry.name) or ('.zip' in entry.name):
                print(entry.name)
                song_list.append(entry.name)

    os.chdir(SPOTIFY_FOLDER)
    # save in parent folder with ../{filename.zip} notation
    with zipfile.ZipFile("spotify.zip", mode="w") as archive:
        for song in song_list:
            print(song)
            archive.write(song)

def zip_list(song_list: list, album_name: str):
    os.chdir(MUSIC_FOLDER)
    # save in parent folder with ../{filename.zip} notation
    with zipfile.ZipFile(f"{album_name}.zip", mode="w") as archive:
        for song in song_list:
            if ('.mp3' in song) or ('.m4a' in song):
                print(song)
                archive.write(song)

def dl(spoturl):
    # flash("Download in progress. Please wait")
    os.chdir(SPOTIFY_FOLDER)
    os.system(f"~/.local/bin/spotdl --format m4a --preload --threads 4 {spoturl}")
    zip_dir()
    move_files()

    # list_songs()

def list_songs():
    os.chdir('/data/music')
    os.system(f"for file in *.mp3 do echo $file done")
    subprocess.run("for song in *.m*; do echo $song; done", shell=True, check=True)

def make_music_list(spoturl):

    music_list = []

    CLIENT_ID = os.getenv("SPOTIFY_ID_KEY")
    CLIRENT_SECRET = os.getenv("SPOTIFY_SECRET_KEY")
    
    sp = spotipy.Spotify(auth_manager=SpotifyClientCredentials(CLIENT_ID, CLIRENT_SECRET))

    
    album_title = sp.album(spoturl)

    #results = sp.album_tracks(album_id, limit, offset, market)

    album = sp.album_tracks(spoturl)

    album_title = album_title['name']

    for songs in album['items']:
        music_list.append(songs["artists"][0]["name"] + " - " + songs['name'] + ".m4a")
        
    #print(album_title)
    #print(music_list) 

    zip_list(music_list, album_title)


    

make_music_list()