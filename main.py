import os

from downloader import DownloaderAudio, DownloaderVideo

downloader = None

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

only_audio = input("Only Audio ( y/N ): ").lower()

print("Choose File type to export log: [ txt | csv ] ( Default is 'txt' )")
log_type = input("Your choice: ")

if only_audio == 'y':
    downloader = DownloaderAudio(link, is_playlist, resolution, folder, path, file_tupe_log=log_type)
elif only_audio == 'n':
    downloader = DownloaderVideo(link, is_playlist, resolution, folder, path, file_tupe_log=log_type)
else:
    print(f"Format not valid. Your awnser was: {only_audio}")
    exit(0)

downloader.download()
