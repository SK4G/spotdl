import os
import subprocess

# class Spot:
#     def dl():
#         os.system(f"~/.local/bin/spotdl {spoturl}")
def dl(spoturl):
    os.system(f"~/.local/bin/spotdl --format m4a {spoturl}")
    list_songs()

def list_songs():
    os.system(f"for file in *.mp3 do echo $file done")
    subprocess.run("for song in *.m*; do echo $song; done", shell=True, check=True)

