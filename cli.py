from ast import arg
import os

from argparse import ArgumentParser
from configparser import ConfigParser

from downloader import DownloaderAudio, DownloaderVideo


class VideoDownloaderCLI:
    def __init__(self, file_config: str = "./env.ini") -> None:
        self._config = ConfigParser()

        self._version = "1.0.0"

        self._link_video_example = ""
        self._link_playlist_example = ""

        self.link_video = ""
        self.link_playlist = ""

        self.audio_only = False
        self.video_only = True

        self.is_playlist = False
        self.folder_output = ""
        self.path_output = ""
        self.resolution = ""
        self.type_log = ""

        self.downloader = None

        self.__load_config(file_config)
        self.__load_links_examples()
        self.set_version()

        self.__run()

    def __load_config(self, file_config: str) -> None:
        self._config.read(file_config)

    def __load_links_examples(self) -> None:
        self._link_video_example = self._config["EXAMPLES_LINKS"]["link_video_example"]
        self._link_playlist_example = self._config["EXAMPLES_LINKS"]["link_playlist_example"]

    def __run(self):
        self.args_parser = ArgumentParser(
            prog="Requirements Installer",
            description="Automação para instalação dos requirements",
            epilog="Desenvolvido por: Pedro Augusto Barbosa Aparecido",
            usage="%(prog)s [OPTIONS...] [VALUES...]"
            
        )

        self.args_parser.version = self.version
        self.args_parser.add_argument("-v", "--version", help="Show CLI Version", action="version")
        self.args_parser.add_argument("-l", "--link", help="Pass link of video to download", action="store", type=str, default=self._link_video_example, required=False)
        self.args_parser.add_argument("-lp", "--link-playlist", help="Pass link of playlist to download", action="store", type=str, default=self._link_playlist_example, required=False)
        self.args_parser.add_argument("-a", "--audio-only", help="Pass if you want only audio", action="store_true", default=False, required=False)
        self.args_parser.add_argument("-vd", "--video-only", help="Pass if you want only video", action="store_true", default=False, required=False)
        self.args_parser.add_argument("-p", "--playlist", help="Pass if is playlist", action="store_true", default=False, required=False)
        self.args_parser.add_argument("-f", "--folder-output", help="Pass name folder output", action="store", type=str, default="VideoYoutube", required=False)
        self.args_parser.add_argument("-ph", "--path-output", help="Pass path output", action="store", type=str, default=os.path.join(os.path.expanduser("~"), "Documents"), required=False)
        self.args_parser.add_argument("-r", "--resolution", help="Pass Video Resolution", action="store", type=str, default="hightest", required=False)
        self.args_parser.add_argument("-tl", "--type-log", help="Pass Type File Log", action="store", type=str, default="txt", required=False)

        args = self.args_parser.parse_args()

        if args:
            try:
                if args.audio_only:
                    self.video_only = False
                    self.audio_only = True
                if not args.audio_only and args.video_only:
                    self.audio_only = False
                    self.video_only = True
                if args.link:
                    self.link_video = args.link
                if args.link_playlist:
                    self.args.link_playlist
                if args.playlist:
                    self.is_playlist = args.playlist
                if args.folder_output:
                    self.folder_output = args.folder_output
                if args.path_output:
                    self.path_output = args.path_folder
                if args.resolution:
                    self.resolution = args.resolution
                if args.type_log:
                    self.type_log = args.type_log
                else:
                    ...

                if self.audio_only:
                    self.downloader = DownloaderAudio(self.link, self.is_playlist, self.resolution, self.folder_output, self.path_output, file_tupe_log=self.type_log)
                else:
                    self.downloader = DownloaderVideo(self.link, self.is_playlist, self.resolution, self.folder_output, self.path_output, file_tupe_log=self.type_log)
                self.downloader.download()

            except:
                self.args_parser.print_help()
                exit(0)

    def set_version(self) -> None:
        self._version = self._config["DEFAULT"]["version"]

    @property
    def version(self) -> str:
        return self._version


if __name__ == "__main__":
    video_downloader_cli = VideoDownloaderCLI("./env.ini")
