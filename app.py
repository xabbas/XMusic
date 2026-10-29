import gi

gi.require_version("Gtk", "4.0")
from gi.repository import Gtk  # type: ignore

from song import Song
from library import Library
from pathlib import Path

class MyWindow(Gtk.ApplicationWindow):
    def __init__(self, **kargs):
        super().__init__(**kargs, title="Hareep")

        settings = Gtk.Settings.get_default()
        settings.set_property("gtk-application-prefer-dark-theme", True)

        self.set_default_size(400, 500)

        self.mainBox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=10)
        self.mainBox.set_valign(Gtk.Align.CENTER)
        self.mainBox.set_margin_top(20)
        self.mainBox.set_margin_end(20)
        self.mainBox.set_margin_bottom(20)
        self.mainBox.set_margin_start(20)
        self.set_child(self.mainBox)

        self.songBox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=10)
        self.songBox.set_halign(Gtk.Align.CENTER)

        self.controlsBox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=20)
        self.controlsBox.set_halign(Gtk.Align.CENTER)

        self.artwork = Gtk.Image(pixel_size=300)
        self.song = Gtk.Label(label="Nothing playing")

        self.previous = Gtk.Button(label="⏪")
        self.previous.connect("clicked", self.onPrevious)

        self.play = Gtk.Button(label="▶️")
        self.play.connect("clicked", self.onPlay)
        self.is_playing = False

        self.next = Gtk.Button(label="⏭️")
        self.next.connect("clicked", self.onNext)

        self.folderButton = Gtk.Button(label="Select a Folder")
        self.folderButton.connect("clicked", self.onFolderButton)

        self.songBox.append(self.artwork)
        self.songBox.append(self.song)

        self.controlsBox.append(self.previous)
        self.controlsBox.append(self.play)
        self.controlsBox.append(self.next)

        self.mainBox.append(self.songBox)
        self.mainBox.append(self.controlsBox)
        self.mainBox.append(self.folderButton)

        self.tracks = []
        self.current_track_index = 0

    def update_track(self, index):
        track = self.tracks[index]

        if self.is_playing:
            self.song.set_label(f"{track.title} - {track.artist}")
        else:
            self.song.set_label(f"Paused: {track.title} - {track.artist}")

    def onPlay(self, _widget):
        if self.is_playing:
            self.is_playing = False
            self.update_track(self.current_track_index)
            self.play.set_label("▶️")

        else:
            self.is_playing = True
            self.update_track(self.current_track_index)
            self.play.set_label("⏸️")

    def onPrevious(self, _widget):
        self.current_track_index = (self.current_track_index - 1) % len(self.tracks)
        self.is_playing = True
        self.update_track(self.current_track_index)
        self.play.set_label("⏸️")

    def onNext(self, _widget):
        self.current_track_index = (self.current_track_index + 1) % len(self.tracks)
        self.is_playing = True
        self.update_track(self.current_track_index)
        self.play.set_label("⏸️")

    def onFolderButton(self, _widget):
        dialog = Gtk.FileDialog()
        dialog.set_title("Select a Folder")

        dialog.select_folder(self, None, self.onFolderSelected)
    def onFolderSelected(self, dialog, result):
        try:
            folder = dialog.select_folder_finish(result)
            self.getTracks(folder.get_path())
        except gi.repository.GLib.Error:  # type: ignore
            pass
    
    def getTracks(self, path: Path):
        library = Library(path)
        tracks = library.getTracks()

        for track in tracks:
            song = Song(track)
            self.tracks.append(song)

def on_activate(app):
    win = MyWindow(application=app)
    win.present()


app = Gtk.Application(application_id="com.xabbas.XMusic")
app.connect("activate", on_activate)

app.run(None)
