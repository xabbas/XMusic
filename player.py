from pathlib import Path
import gi

gi.require_version("Gst", "1.0")
from gi.repository import GLib, Gst #type:ignore

class Player:
    def __init__(self, path: Path):
        self.path = path
        
    def play(self):
        Gst.init(None)

        self.playerBin = Gst.ElementFactory.make("playbin", "playerbin")
        trackUri = Gst.filename_to_uri(self.path)
        self.playerBin.set_property("uri", trackUri)
        self.playerBin.set_state(Gst.State.PLAYING)
        self.playerLoop = GLib.MainLoop().run()
        
        self.playerLoop.run()
    def pause(self):
        self.playerBin.set_state(Gst.State.NULL)