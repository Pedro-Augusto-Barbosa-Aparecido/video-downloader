import os

from moviepy.editor import VideoFileClip, AudioFileClip
from tqdm import tqdm


class ConverterMP3:
    def __init__(self, filepath: str, is_many: bool = False) -> None:
        self.path = filepath
        self.is_many = is_many
        print("filepath: ", end="")
        print(filepath)
        self.audio_converter = None

        self.video_clip: VideoFileClip = VideoFileClip(filepath)
        self.videos_clips: list[VideoFileClip] = []

    def _get_filename_and_path(self):
        return f"{self.path}\\{self.filename}"

    def _get_video_clip(self):
        self.video_clip = VideoFileClip(self.path)    
        
    def _get_videos_clips(self, files: list[str]) -> list[AudioFileClip]:
        _files: list[AudioFileClip] = []
        for file in tqdm(files):
            _files.append(VideoFileClip(file).audio)

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

    def _converter_many_audio(self, files: list[str], path_folder: str = None):
        _files = self._get_videos_clips(files)
        _files_names = os.listdir(files[0].split("\\")[len(files[0].split("\\")) - 1])
        
        for audio, file in tqdm(zip(_files, _files_names)):
            audio.write_audiofile(f"{path_folder}\\{file.replace('.mp4', '.mp3')}")

    def init(self):
        if not self.is_many:
            # self._get_video_clip()
            ...
        else:
            ...

    def converter(self, many: bool = False, files: list[str] = None, path_folder: str = None):
        if many:
            self._converter_many_audio(files, path_folder)
        else:
            self._converter_one_audio()


if __name__ == "__main__":
    # path = "C:\\Users\\pedro\\Documents\\TesteDownload\\Rap_do_Shikamaru_(Naruto)_CUIDADO_COM_AS_SOMBRAS_NERDHITS.mp4"
    converter = ConverterMP3(os.path.join(os.path.expanduser("~"), "Documents\\TesteDownload\\CENAS BIZZARAS E ENGRAÇADAS DOS ANIMES.mp4"),
                    False)

    converter.init()
    converter.converter()

    # VideoFileClip(path).audio.write_audiofile(path.replace(".mp4", ".mp3"))
    
