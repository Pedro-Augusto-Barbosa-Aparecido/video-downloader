from pytube import Playlist, YouTube

class Downloader:
    def __init__(self, link: str, is_playlist: bool = False) -> None:
        self.link = link
        self.is_playlist = is_playlist
        self.videos = []

        self.playlist = None
        self.youtube_video = None

        if is_playlist:
            self.playlist = self._get_playlist(link)
        else:
            self.youtube_video = self._get_youtube_video(link)

    def __str__(self):
        if self.is_playlist:
            return f"Playlist: {self.playlist.title}"
        return f"Video: {self.youtube_video.title}"

    def __len__(self):
        if self.is_playlist:
            return len(self.playlist.videos)
        return 1

    def _get_playlist(self, link: str):
        return Playlist(link)

    def _get_youtube_video(self, link: str):
        return YouTube(link)
