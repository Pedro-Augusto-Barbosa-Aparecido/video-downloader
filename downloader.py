import os
import calendar
import time

from typing import Any
from pytube import Playlist, YouTube
from pytube.cli import on_progress
from colorama import Fore, Style
from pathlib import Path

class Downloader:
    def __init__(self, link: str, is_playlist: bool = False) -> None:
        self.link = link
        self.is_playlist = is_playlist
        self.videos: list[YouTube] = []

        self.playlist = None
        self.youtube_video = None
        self.path_output = None

        self.videos_completed: dict = []

    def __str__(self):
        if self.is_playlist:
            return f"Playlist: {self.playlist.title}"
        return f"Video: {self.youtube_video.title}"

    def __len__(self):
        if self.is_playlist:
            return len(self.playlist.videos)
        return 1

    def __repr__(self) -> str:
        if self.is_playlist:
            return self.playlist.title
        return self.youtube_video.title

    def _get_playlist(self, link: str):
        return Playlist(link)

    def _get_youtube_video(self, link: str):
        return YouTube(link)

    def _get_videos_by_playlist(self):
        for video in self.playlist:
            self.videos.append(YouTube(video, on_progress_callback=on_progress, on_complete_callback=self._on_complete_donwload))

    def _get_file_size(self, size: int = 0, format: bool = False):
        if format:
            return f"{(size / 1_000_000.0):.2f} MB/s"
        return f"{size} Bytes"

    def _print_current_video_downloading(self, video_detail: dict[str, Any] = None):
        if video_detail is None:
            raise Exception("Video Detail is None, please verify your stream.")

        print("Downloading...", end="")
        print(f"    Video: {video_detail['title']}")
        print(f"File Size: {self._get_file_size(video_detail['file_size'], True)} | Waiting downloading!")

    def _finish_all_downloads(self, videos_opt: list[dict[str, Any]], total: int, success_and_fails: dict[str, int]): 
        print(f"Downloads complete, total: {total}")
        print(f"Success: {success_and_fails['success']} - Fails: {success_and_fails['fails']}")
        for video in videos_opt:
            print(Fore.GREEN + Style.BRIGHT + f"Title: {video['title']}")
            print(Fore.YELLOW + Style.BRIGHT + f"File Size Final: {self._get_file_size(video['file_size'], True)}")
            print(Fore.BLUE + Style.BRIGHT + f"Path | File Location: {video['path_on_system']}\\{video['title']}{'mp4' if video['title'][len(video['title']) - 1] == '.' else '.mp4' }")
            print(Fore.BLACK + " -------------------------- " + Style.RESET_ALL)

    @staticmethod
    def _on_complete_donwload(self, file_path):
        file_path = file_path.split("\\")
        print(f"Video '{file_path[len(file_path) - 1]}' has completed.")

    @staticmethod
    def _generate_log(videos_completed: list[dict], videos: list[YouTube]):
        try:
            ...
        except FileNotFoundError as fn:
            print(fn.args)
            
    def init(self, folder: str, path: str = None):
        if self.is_playlist:
            self.playlist = self._get_playlist(self.link)
            self._get_videos_by_playlist()
        else:
            self.youtube_video = self._get_youtube_video(self.link)

        self.set_folder_output(folder, path)

    def set_folder_output(self, folder: str, path: str = None):
        self.folder_output = folder

        if path is None:
            self.path_output = os.path.join(os.path.expanduser("~"), "Documents")
        else:
            self.path_output = path

    def video_length(self, video: YouTube):
        return video.length

    def download_playlist(self, generate_logs: bool = False, keep_old_log: bool = False):
        videos_completed = []
        videos_log = []

        for video in self.videos:
            videos_log.append(video)
            try:
                stream = video.streams.get_highest_resolution()
                stream_detail = { 
                    "title": stream.title, 
                    "file_size": stream.filesize, 
                    "path": stream.get_file_path(), 
                    "path_on_system": f"{self.path_output}\\{self.folder_output}"

                }

                self._print_current_video_downloading(stream_detail)

                stream.download(output_path=os.path.join(self.path_output, self.folder_output))
                videos_completed.append(stream_detail)
            except Exception as e:
                print(e.args)

        self.videos_completed = videos_completed
        # self._generate_log(videos_completed, videos_log)
        self._finish_all_downloads(videos_completed, self.__len__(), { "success": len(videos_completed), "fails": self.__len__() - len(videos_completed) })

    def download_video(self, generate_logs: bool = False, keep_old_log: bool = False):
        videos_completed = []

        try:
            video = self.youtube_video.streams.get_highest_resolution()
            video_detail = { 
                "title": video.title, 
                "file_size": video.filesize, 
                "path": video.get_file_path(), 
                "path_on_system": f"{self.path_output}\\{self.folder_output}"

            }

            self._print_current_video_downloading(video_detail)
            video.download(output_path=os.path.join(self.path_output, self.folder_output))
            videos_completed.append(video_detail)

            self.videos_completed = videos_completed
            
        except Exception as e:
            print(e.args)

        self._finish_all_downloads(videos_completed, self.__len__(), { "success": len(videos_completed), "fails": self.__len__() - len(videos_completed) })


class DownloaderLogger:
    TYPES_OUTPUT_LOG = ("txt", "csv")
    REGEX_FILE_EXTENSION = "\.txt$|\.csv$"

    def __init__(self, filename: str = "log", use_timestamp: bool = False) -> None:
        self.filename = filename
        self.use_timestamp = use_timestamp

        self.dir_output_log = os.path.join(os.path.curdir, "log")
        self.type_output_log = "txt"

        self.file = self.get_file_path(self.dir_output_log, self.filename, self.type_output_log)
        self._create_the_log_file()

    def _get_current_timestamp(self):
        return calendar.timegm(time.gmtime())

    def _create_the_log_file(self):
        if self.use_timestamp:
            if not os.path.isdir(f"{os.path.curdir}\\log"):
                os.mkdir(f"{os.path.curdir}\\log")
            _filename = self.file.replace(f".{self.type_output_log}", '')
            file_time = Path(f"{_filename}_{self._get_current_timestamp()}.{self.type_output_log}")
            file_time.touch(exist_ok=True)
        else:
            try:
                with open(f"{self.file}", 'r+') as file:
                    pass
            except FileNotFoundError:
                if not os.path.isdir(f"{os.path.curdir}\\log"):
                    os.mkdir(f"{os.path.curdir}\\log")
                file = Path(self.file)
                file.touch(exist_ok=True)

    def get_file_path(self, output_path: str, filename: str, type_file: str):
        return os.path.join(output_path, f"{filename}.{type_file}")

if __name__ == "__main__":
    logger = DownloaderLogger(use_timestamp=True)
