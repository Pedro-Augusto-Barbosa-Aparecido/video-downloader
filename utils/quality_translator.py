class Quality:
    def __init__(self, quality: str = "high") -> None:
        self.quality = quality
        self._quality_translate: str = None

        self.translate()

    @property
    def resolution(self) -> str:
        return self._quality_translate

    def translate(self) -> None:
        if self.quality == "high":
            self._quality_translate = "720p"
        elif self.quality == "hightest":
            self._quality_translate = "1080p"
        elif self.quality == "medium":
            self._quality_translate = "480p"
        elif self.quality == "low_medium":
            self._quality_translate = "360p"
        elif self.quality == "low":
            self._quality_translate = "240p"
        elif self.quality == "lowest":
            self._quality_translate = "144p"
        else:
            self.quality = "hightest"
            self._quality_translate = "1080p"
