https://github.com/SK4G/spotdl
https://docs.google.com/document/d/1tdWUZKESoKO_Y48A25rujtj6Ms31ao_JRo1CS7kG3AE/edit?usp=sharing

Examples of things you enjoyed about or learned from this project
  - The open nature of the project where as long as we met the technical requirements we could implement anything we wanted. 
  - Using python as the server logic instead of javascript. Python has a lot of modules to streamline implementations.
  - How to serve users files for download

Examples of things you didn’t enjoy or wanted to learn from this project
  - The python module used as the download client spotdl does not have up to date information on developer or API usage.
    Due to this we had to use spotdl from the command line with os.system(spotd --args url).
    https://stackoverflow.com/questions/65240392/how-can-i-use-spotdl-inside-python
    https://github.com/ritiek/spotify-downloader/blob/master/docs/source/api.rst
  - Due to time constraints, did not look into how to parse metadata from a spotify url. 
    To bypass this, regardless of whether songs are already downloaded to server or not, they are downloaded to a temporary directory, to separate them from the already downloaded songs.
    Afterwards, a zip archive of the songs from the spotify url is created, then songs and zip is moved to the global music folder. 
  - Would have liked to parse the songs in a given spotify url and create a list in format "{artists} - {title}.{output-ext}"
    With this list the songs could have been checked to see if they already existed in the global music folder. 
    Then a zip archive based on the song list would have been created, with a unique zip {album}.zip name. As is the archive name is always spotify.zip, always being overwritten per url download request.
    An unused function was left for this functionality in  spotmodule.py      zip_list(song_list: list, album_name: str):
  - Would have liked to dynamically embed a music player based on spotify url or a music player based on the server music library. 
  
Technical Requirements
  - Flask server
  - Postgress DB
  - User login
  - Beautification

Stretch Features
  - KooDb3sIr3EwE9j This stretch feature allows users to upload and download music files to the site. Users can enter a Spotify URL and download a song. Users can also upload an mp4/m4a file from their local computer.
  - KnaHA8wArzKrQ0g Instead of downloading a single file at a time, this stretch feature allows you to zip all songs from a given spotify url and download all files at once.
