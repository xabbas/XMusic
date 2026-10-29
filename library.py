from pathlib import Path

class Library():
    def __init__(self, path: str):
        self._path = Path(path).resolve()
        self._tracks = []        


    def getTracks(self):
        self._findTracks()
        return self._tracks
    
    def _findTracks(self):
        for item in self._path.iterdir():
            if item.name.startswith("."):
                continue
            if item.is_dir():
                self._isDir(item)
            else:
                self._isFile(item)

    def _isFile(self, path: Path):
        suffixes = [".mp3", ".ogg", ".flac", ".wav", ".m4a"]
        
        if path.suffix.lower() in suffixes:
            self._tracks.append(path.resolve())

    def _isDir(self, path: Path):
        for item in path.iterdir():
            
            if Path(item).is_dir():
                self._isDir(item)
            else:
                self._isFile(item)