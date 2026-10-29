from tinytag import TinyTag
from pathlib import Path

class Song:
    def __init__(self, path: Path, **kwargs):
        self.filepath = path
        tags = TinyTag.get(path).as_dict()

        try:
            self.artist = tags["artist"][0]
            self.album = tags["album"][0]
            self.title = tags["title"][0]
            self.year = tags["year"][0]
        except KeyError as e:
            pass

