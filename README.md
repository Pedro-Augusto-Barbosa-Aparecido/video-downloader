<div align="center">
    <img align="center" src="./img/logo_readme.png">
</div>

# Video Downloader

<p align="center"> 🚧 Application in construction 🚧 </p>

## Installation and First run

 - Creating virtual environment:
   - `pip install venv`
   - `python -m venv $venv-name`
   - `pip install -r requirements.txt`
 - Connecting to venv:
   - `$path_venv/Scripts/Activate.ps1`
 - Running project:
   - `python ./main.py`

## Features

 - [x] Download video on high quality ( if not has resolution passed, app gets closer to past resolution )
   - [x] Quality 144p lowest
   - [x] Quality 240p low
   - [x] Quality 360p low_medium
   - [x] Quality 480p mediun
   - [x] Quality 720p high
   - [x] Quality 1080p hightest
 - [x] Download Mídia Type
   - [x] Video
   - [x] Playlist
   - [x] Only Video Áudio
   - [x] Only Playlist Videos Áudio
 - [x] Save video anywhere
   - [x] Default folder path ( ***User/Documents*** )
   - [x] Default folder name ( ***VideoYoutube*** )
   - [x] Dynamics folder path
   - [x] Dynamics folder name
 - [x] Export log
   - [x] Type export file
     - [x] ``.txt``
       - [x] Filename start with: ( ***log*** )
         - [x] End with timestamp
         - [x] End without timestamp
     - [x] ``.csv``
       - [x] Filename start with: ( ***log*** )
         - [x] End with timestamp
         - [x] End without timestamp
   - Folder log export ```$project_folder/log```
 - [ ] GUI

## Bugs to FIX

 - [ ] `NoneType has no attribute streams`
    <div align="center">
      <img src="./img/bug_tainara.png">
    </div>
