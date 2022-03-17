import os
import calendar
import sys
import time
import codecs
import pyttsx3

from typing import Any
from datetime import datetime
from pytube import Playlist, YouTube
from pytube.cli import on_progress
from colorama import Fore, Style
from pathlib import Path
from tqdm import tqdm

from utils.quality_translator import Quality

class Downloader:
    def __init__(self, link: str, is_playlist: bool = False, quality: str = "high") -> None:
        self.link = link
        self.is_playlist = is_playlist
        self.videos: list[YouTube] = []

        self.playlist = None
        self.youtube_video = None
        self.path_output = None

        self.videos_completed: dict = []
        self.generator_log = DownloaderLogger(use_timestamp=True)

        self.voice_speaker = pyttsx3.init()
        self.quality = Quality(quality)

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
            self.videos.append(YouTube(video, on_complete_callback=self._on_complete_donwload))

    def _get_file_size(self, size: int = 0, format: bool = False):
        if format:
            return f"{(size / 1024.0 / 1024.0):.2f} MB/s"
        return f"{size} Bytes"

    def _print_current_video_downloading(self, video_detail: dict[str, Any] = None):
        if video_detail is None:
            raise Exception("Video Detail is None, please verify your stream.")

        print("Downloading...", end="")
        print(f"    Video: {video_detail['title']}")
        print(f"File Size: {self._get_file_size(video_detail['file_size'], True)} | Resolution: {video_detail['resolution']} | Waiting downloading!")

    def _finish_all_downloads(self, videos_opt: list[dict[str, Any]], total: int, success_and_fails: dict[str, int]): 
        print(f"Downloads complete, total: {total}")
        print(f"Success: {success_and_fails['success']} - Fails: {success_and_fails['fails']}")
        for video in videos_opt:
            print(Fore.GREEN + Style.BRIGHT + f"Title: {video['title']}")
            print(Fore.YELLOW + Style.BRIGHT + f"File Size Final: {self._get_file_size(video['file_size'], True)}")
            print(Fore.BLUE + Style.BRIGHT + f"Path | File Location: {video['path_on_system']}\\{video['title']}{'mp4' if video['title'][len(video['title']) - 1] == '.' else '.mp4' }")
            print(Fore.BLACK + " -------------------------- " + Style.RESET_ALL)

        message = ""

        if (success_and_fails["fails"] > 0) and self.is_playlist:
            message = "Playlist baixada, porém houve videos que não deram certo. Verifique seus links e sua conexão com a rede. "
        elif (success_and_fails["success"] == len(videos_opt)) and self.is_playlist:
            message = "Playlist baixada com sucesso. Verifique o diretório que você escolheu para salvar os videos."
        elif not (self.is_playlist) and (success_and_fails["fails"] > 0):
            message = "Ocorreu algum erro durante o download, por favor verifique o link e sua conexão com a rede."
        elif not (self.is_playlist) and (success_and_fails["success"] == len(videos_opt)):
            message = "Video baixado com sucesso, verifique o diretório escolhido para o mesmo."
        else:
            message = "Inconsistência na execução do programa reinicie ele ou reinicie o computador."

        self._alert_on_complete(message)

    @staticmethod
    def _on_complete_donwload(self, file_path):
        file_path = file_path.split("\\")
        print(f"Video '{file_path[len(file_path) - 1]}' has completed.")

    def _alert_on_complete(self, msg: str) -> None:
        self.voice_speaker.say(msg)
        self.voice_speaker.runAndWait()

    def _show_progress_bar(self, stream, _chunk, bytes_remaining):
        current = ((stream.filesize - bytes_remaining) / stream.filesize)
        percent = ('{0:.1f}').format(current * 100)
        progress = int(50 * current)
        status = '█' * progress + '-' * (50 - progress)
        sys.stdout.write(' ↳ |{bar}| {percent}%\r'.format(bar=status, percent=percent))
        sys.stdout.flush()
            
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

    def download_playlist(self, generate_logs: bool = True, keep_old_log: bool = True):
        videos_completed = []
        videos_log = []

        for video in self.videos:
            video.register_on_progress_callback(self._show_progress_bar)
            videos_log.append(video)
            try:
                stream = video.streams.get_by_resolution(self.quality.resolution)
                stream_detail = { 
                    "title": stream.title, 
                    "file_size": stream.filesize, 
                    "path": stream.get_file_path(), 
                    "resolution": video.resolution,
                    "path_on_system": f"{self.path_output}\\{self.folder_output}"

                }

                self._print_current_video_downloading(stream_detail)

                stream.download(output_path=os.path.join(self.path_output, self.folder_output))
                videos_completed.append(stream_detail)
            except Exception as e:
                print(e.args)

        self.videos_completed = videos_completed

        if generate_logs: 
            print(f"Exporting log in {os.path.realpath(self.generator_log.file)}")
            timestamp = True if not keep_old_log else False
            self.generator_log.generate_log(videos_completed, keep_old_log=keep_old_log, timestamp=timestamp)

        self._finish_all_downloads(videos_completed, self.__len__(), { "success": len(videos_completed), "fails": self.__len__() - len(videos_completed) })

    def download_video(self, generate_logs: bool = True, keep_old_log: bool = True):
        videos_completed = []

        try:
            self.youtube_video.register_on_progress_callback(self._show_progress_bar)
            video = self.youtube_video.streams.get_by_resolution(self.quality.resolution)
            if video is None:
                video = self.youtube_video.streams.get_lowest_resolution() if self.quality.quality in ["low", "lowest", "low_medium"] else self.youtube_video.streams.get_highest_resolution()

            video_detail = { 
                "title": video.title, 
                "file_size": video.filesize, 
                "path": video.get_file_path(), 
                "resolution": video.resolution,
                "path_on_system": f"{self.path_output}\\{self.folder_output}"

            }

            self._print_current_video_downloading(video_detail)
            video.download(output_path=os.path.join(self.path_output, self.folder_output))
            videos_completed.append(video_detail)

            self.videos_completed = videos_completed
            
        except Exception as e:
            print(e.args)

        if generate_logs:
            print(f"Exporting log in {os.path.realpath(self.generator_log.file)}")
            timestamp = True if not keep_old_log else False
            self.generator_log.generate_log(videos_completed, keep_old_log=keep_old_log, timestamp=timestamp)

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
        self.file_path = ""
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
            
            self.file_path = f"{_filename}_{self._get_current_timestamp()}.{self.type_output_log}"

        else:
            try:
                with open(f"{self.file}", 'r+') as file:
                    pass
            except FileNotFoundError:
                if not os.path.isdir(f"{os.path.curdir}\\log"):
                    os.mkdir(f"{os.path.curdir}\\log")
                file = Path(self.file)
                file.touch(exist_ok=True)

            self.file_path = self.file

    def _get_keys(self, dict: dict):
        return list(dict.keys())

    def _write_date(self, logger_file):
        logger_file.write("======================================\n")
        logger_file.write(f"======{datetime.now()}======\n")
        logger_file.write("======================================\n\n")

    def get_file_path(self, output_path: str, filename: str, type_file: str):
        return os.path.join(output_path, f"{filename}.{type_file}")

    def generate_log(self, video_dict_to_log: list[dict[str, Any]] = None, timestamp: bool = True, keep_old_log: bool = True):
        if video_dict_to_log is None:
            try:
                os.remove(self.file_path)
            except Exception as e:
                print(e.args)

            raise ValueError("Invalid content to export log.")

        if keep_old_log and not timestamp:
            with codecs.open(self.file_path, "a+", "utf-8") as logger_file:
                self._write_date(logger_file)
                for item in tqdm(video_dict_to_log):
                    logger_file.write(f"Title: {item['title']}\n")
                    logger_file.write(f"File Size: {item['file_size']}\n")
                    logger_file.write(f"Resolution: {item['resolution']}\n")
                    logger_file.write(f"File Location: {item['path_on_system']}\n")
                    logger_file.writelines("---------------------------------------\n\n")

                    time.sleep(1 / len(video_dict_to_log))
        else:
            with codecs.open(self.file_path, "w+", "utf-8") as logger_file:
                self._write_date(logger_file)
                for item in tqdm(video_dict_to_log):
                    logger_file.write(f"Title: {item['title']}\n")
                    logger_file.write(f"File Size: {item['file_size']}\n")
                    logger_file.write(f"Resolution: {item['resolution']}\n")
                    logger_file.write(f"File Location: {item['path_on_system']}\n")
                    logger_file.writelines("---------------------------------------\n\n")

                    time.sleep(1 / len(video_dict_to_log))
                


if __name__ == "__main__":
    # d = [
    #     { "title": "Teste 1", "file_size": "400Mb", "path_on_system": "Documents/" },
    #     { "title": "Teste 2", "file_size": "400Mb", "path_on_system": "Documents/" },
    #     { "title": "Teste 3", "file_size": "400Mb", "path_on_system": "Documents/" },
    #     { "title": "Teste 4", "file_size": "400Mb", "path_on_system": "Documents/" },
    # ]
    # logger = DownloaderLogger(use_timestamp=True)
    # logger.generate_log(d, timestamp=True)

    downloader = Downloader(link="https://www.youtube.com/watch?v=DiXbJL3iWVs", is_playlist=False, quality="hightest")
    downloader.init("VideoYoutube", os.path.join(os.path.expanduser("~"), "Documents"))
    downloader.download_video()
