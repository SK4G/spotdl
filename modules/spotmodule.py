from zipfile import ZipFile
import zipfile
import os
import subprocess
import shutil
# from flask import flash


MUSIC_FOLDER =  os.path.join(os.getcwd(), 'music')
SPOTIFY_FOLDER =  os.path.join(os.getcwd(), 'spotify')

# MUSIC_FOLDER =  os.path.join(os.getcwd(), MUSIC_FOLDER)

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

def zip_all(folder):
    song_list = []
    print(os.getcwd())
    print(SPOTIFY_FOLDER)
    # append mp3 or m4a files in specified directory
    for entry in os.scandir(f"{folder}"):
        if entry.is_file():
            if ('.mp3' in entry.name) or ('.m4a' in entry.name) or ('.zip' in entry.name):
                print(entry.name)
                song_list.append(entry.name)

    os.chdir(folder)
    # save in parent folder with ../{filename.zip} notation
    with zipfile.ZipFile(f"{folder}.zip", mode="w") as archive:
        for song in song_list:
            print(song)
            archive.write(song)
    return None

def dl(spoturl):
    # flash("Download in progress. Please wait")
    # shutil.rmtree(SPOTIFY_FOLDER)
    # os.mkdir(SPOTIFY_FOLDER)
    os.chdir(SPOTIFY_FOLDER)
    os.system(f"~/.local/bin/spotdl --format m4a --preload --threads 4 {spoturl}")
    # zip spoturl songs
    os.chdir("..")
    zip_all("spotify")
    move_files()

    # list_songs()

def list_songs():
    os.chdir('music')
    os.system(f"for file in *.mp3 do echo $file done")
    subprocess.run("for song in *.m*; do echo $song; done", shell=True, check=True)

