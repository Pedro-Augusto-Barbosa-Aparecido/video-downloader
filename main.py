import os
from pydoc import resolve

from downloader import Downloader

is_playlist = input("Do you want download a playlist? ( y/N ) ").lower()

if is_playlist == 'y':
    is_playlist = True
elif is_playlist == 'n':
    is_playlist = False
else:
    print(f"Format not valid, valid only Video or Playlist. Your awnser was: {is_playlist}")
    exit(0)

link = input("Enter with youtube link: ")
path = input("Enter with a path or press enter ( default is Documents Folder ): ")

if path != "":
    if not os.path.exists(path):
        raise ValueError("Invalid Path")
else:
    path = os.path.join(os.path.expanduser("~"), "Documents")

folder = input("Enter the folder to save video(s) ( default is 'VideosYoutube' ): ")

if folder == "":
    folder = "VideoYoutube"

print("Choose resolution: lowest=144p | low=240p | low_medium=360p | medium=480p | high=720p | hightest=1080p")
resolution = input("Your choice: ")

downloader = Downloader(link, is_playlist, resolution)
downloader.init(folder, path)

if is_playlist:
    downloader.download_playlist()
else:
    downloader.download_video()
