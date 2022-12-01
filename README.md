https://github.com/SK4G/spotdl

https://docs.google.com/document/d/1tdWUZKESoKO_Y48A25rujtj6Ms31ao_JRo1CS7kG3AE/edit?usp=sharing

https://spotdl.fly.dev

Examples of things you enjoyed about or learned from this project
  - The open nature of the project where as long as we met the technical requirements we could implement anything we wanted. 
  - Using python as the server logic instead of javascript. Python has a lot of modules to streamline implementations.
  - How to serve users files for download

Examples of things you didn’t enjoy or wanted to learn from this project
  - The python module used as the download client spotdl does not have up to date information on developer or API usage.
    Due to this we had to use spotdl from the command line with os.system(spotd --args url).
    https://stackoverflow.com/questions/65240392/how-can-i-use-spotdl-inside-python
    https://github.com/ritiek/spotify-downloader/blob/master/docs/source/api.rst
  - Would have liked to dynamically embed a music player based on spotify url or a music player based on the server music library.
  - Figure out logic to store zip files for x amount of time or per user session.
  
Technical Requirements
  - Flask server  - Luiz
  - Postgress DB  - Luiz
  - User login    - Luiz
  - Used spotipy as REST API - Brandon

Stretch Features
  - KooDb3sIr3EwE9j This stretch feature allows users to upload and download music files to the site. Users can enter a Spotify URL and download a song. Users can also upload an mp4/m4a file from their local computer.
  - KnaHA8wArzKrQ0g Instead of downloading a single file at a time, this stretch feature allows you to zip all songs from a given spotify url and download all files at once.
