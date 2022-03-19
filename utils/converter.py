import os
import shutil

from moviepy.editor import VideoFileClip, AudioFileClip
from tqdm import tqdm


class ConverterMP3:
    def __init__(self, filepath: str, is_many: bool = False) -> None:
        self.path = filepath
        self.is_many = is_many
        print("filepath: ", end="")
        print(filepath)
        self.audio_converter = None

        self.video_clip: VideoFileClip = None
        self.videos_clips: list[VideoFileClip] = []

    def _get_filename_and_path(self):
        return f"{self.path}\\{self.filename}"

    def _get_video_clip(self):
        self.video_clip = VideoFileClip(self.path)    
        
    def _get_videos_clips(self, files: list[str], path: str) -> list[VideoFileClip]:
        _files: list[AudioFileClip] = []
        for file in tqdm(files):
            _files.append(VideoFileClip(f"{path}\\{file}"))

        return _files

    
    def _close(self, audio: AudioFileClip = None, video: VideoFileClip = None):
        if self.is_many and (audio is None) and (video is None):
            audio.close()
            video.close()
        else:
            self.audio_converter.close()
            self.video_clip.close()

    def _converter_one_audio(self):
        self._get_video_clip()

        self.audio_converter = self.video_clip.audio
        self.audio_converter.write_audiofile(self.path.replace(".mp4", ".mp3"))

        self._close()

    def _converter_many_audio(self, files: list[str], path: str, path_folder: str = None):
        audios = []

        for file in files:
            if not ".mp4" in file:
                continue
            _path = f"{path}\\{file.replace('mp4', 'mp3')}"
            audios.append(_path)

            video = VideoFileClip(f"{path}\\{file}")
            audio = video.audio

            audio.write_audiofile(_path)

            audio.close()
            video.close()

        files = os.listdir(path)
        _files = []

        print("Collecting files...")
        for file in tqdm(files):
            if ".mp3" in file:
                _files.append(file)

        for i in tqdm(range(len(audios))):
            shutil.move(audios[i], f"{path_folder}\\{_files[i]}")

    def init(self):
        ...

    def converter(self, many: bool = False, files: list[str] = None, path: str = None, path_folder: str = None):
        if many:
            self._converter_many_audio(files, path, path_folder)
        else:
            self._converter_one_audio()
