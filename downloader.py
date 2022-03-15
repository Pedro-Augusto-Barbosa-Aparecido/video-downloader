import os

from typing import Any
from pytube import Playlist, YouTube
from pytube.cli import on_progress
from colorama import Fore, Style


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

    def init(self, folder: str, path: str = None):
        if self.is_playlist:
            self.playlist = self._get_playlist(self.link)
        else:
            self.youtube_video = self._get_youtube_video(self.link)

        self.set_folder_output(folder, path)
        self._get_videos_by_playlist()

    def set_folder_output(self, folder: str, path: str = None):
        self.folder_output = folder

        if path is None:
            self.path_output = os.path.join(os.path.expanduser("~"), "Documents")
        else:
            self.path_output = path

    def video_length(self, video: YouTube):
        return video.length

    def download_playlist(self, add_on_logs: bool = False, keep_old_log: bool = False):
        videos_completed = []

        for video in self.videos:
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
        self._finish_all_downloads(videos_completed, self.__len__(), { "success": len(videos_completed), "fails": self.__len__() - len(videos_completed) })
