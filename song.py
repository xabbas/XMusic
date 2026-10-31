from tinytag import TinyTag
from pathlib import Path
from gi.repository import GLib, Gdk # type: ignore

class Song:
    def __init__(self, path: Path, **kwargs):
        self.path = path
        song_obj = TinyTag.get(path, image=True)

        try:
            self.artist = song_obj.artist or ""
            self.album = song_obj.album or ""
            self.title = song_obj.title or ""
            self.year = song_obj.year or ""
            self.artwork = song_obj.get_image() or None

            if self.artwork:
                try:
                    glib_bytes = GLib.Bytes.new(self.artwork)
                    self.artwork = Gdk.Texture.new_from_bytes(glib_bytes)
                except Exception as e:
                    print(f"Error compiling image layout: {e}")
        except KeyError as e:
            pass

