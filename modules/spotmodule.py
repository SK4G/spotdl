import os
import subprocess
from flask import flash
from modules.zipsongs import download_all

MUSIC_FOLDER = 'music'

# MUSIC_FOLDER =  os.path.join(os.getcwd(), MUSIC_FOLDER)

def dl(spoturl):
    # flash("Download in progress. Please wait")
    os.chdir('music')
    os.system(f"~/.local/bin/spotdl --m3u --format m4a --preload --threads 1 {spoturl}")
    download_all()
    os.chdir("..")
    list_songs()

def list_songs():
    os.chdir('music')
    os.system(f"for file in *.mp3 do echo $file done")
    subprocess.run("for song in *.m*; do echo $song; done", shell=True, check=True)

