from zipfile import ZipFile
import zipfile
import os
from flask import send_file

# Functions were move to spotmodule.py
# This module is unused

def zip_all(folder):
    song_list = []
    # append mp3 or m4a files in specified directory
    for entry in os.scandir(folder):
        if entry.is_dir() or entry.is_file():
            if ('.mp3' in entry.name) or ('.m4a' in entry.name):
                print(entry.name)
                song_list.append(entry.name)

    os.chdir(folder)
    # save in parent folder with ../{filename.zip} notation
    with zipfile.ZipFile(f"{folder}.zip", mode="w") as archive:
        for song in song_list:
            print(song)
            archive.write(song)

def download_all():
    song_list = []
    # append mp3 or m4a files in specified directory
    for entry in os.scandir('music'):
        if entry.is_dir() or entry.is_file():
            if ('.mp3' in entry.name) or ('.m4a' in entry.name):
                print(entry.name)
                song_list.append(entry.name)
    print(os.getcwd())
    os.chdir('music')
    # save in parent folder with ../{filename.zip} notation
    with zipfile.ZipFile("music.zip", mode="w") as archive:
        for song in song_list:
            print(song)
            archive.write(song)

    return send_file('music.zip',
            mimetype = 'zip',
            attachment_filename= 'music.zip',
            as_attachment = True)


def download_requested(song_list):
    # append songs in specified directory
    for entry in os.scandir('music'):
        if entry.is_dir() or entry.is_file():
            song_list.append(entry.name)

    os.chdir('music')
    # save in parent folder with ../{filename.zip} notation
    with zipfile.ZipFile("music.zip", mode="w") as archive:
        for song in song_list:
            print(song)
            archive.write(song)

    return send_file('music.zip',
            mimetype = 'zip',
            attachment_filename= 'music.zip',
            as_attachment = True)
