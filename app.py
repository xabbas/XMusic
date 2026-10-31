import gi
from pathlib import Path
from song import Song
from library import Library
from player import Player

gi.require_version("Gtk", "4.0")
gi.require_version("Adw", "1")

from gi.repository import Gtk, Adw  # type: ignore

class MyApp(Adw.Application):
    def __init__(self, **kwargs):
        super().__init__(application_id="com.xabbas.XMusic")

        self.tracks = []
        self.current_track_index = 0

    def do_activate(self):
        win = Adw.ApplicationWindow( application=self, default_height=500, default_width=500,  title="XMusic")

        toolbar_view = Adw.ToolbarView()
        header_bar = Adw.HeaderBar()
        toolbar_view.add_top_bar(header_bar)

        mainBox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=20)
        mainBox.set_valign(Gtk.Align.CENTER)
        mainBox.set_halign(Gtk.Align.CENTER)
        mainBox.set_margin_top(20)
        mainBox.set_margin_end(20)
        mainBox.set_margin_bottom(20)
        mainBox.set_margin_start(20)

        self.songBox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=20)
        self.songBox.set_halign(Gtk.Align.CENTER)
        self.songBox.set_valign(Gtk.Align.CENTER)

        self.artwork = Gtk.Box()
        self.artwork.add_css_class("card")
        self.artwork.set_overflow(Gtk.Overflow.HIDDEN)

        self.controlsBox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=15)
        self.controlsBox.set_halign(Gtk.Align.CENTER)
        self.controlsBox.set_valign(Gtk.Align.CENTER)

        self.artwork_image = Gtk.Picture()
        self.artwork_image.set_content_fit(Gtk.ContentFit.COVER)
        self.artwork_image.set_size_request(300, 300)
        self.artwork.append(self.artwork_image)

        self.song = Gtk.Label(label="Nothing playing...")

        self.previous = Gtk.Button(label="⏪")
        self.previous.add_css_class("circular")
        self.previous.set_valign(Gtk.Align.CENTER)
        self.previous.connect("clicked", self.onPrevious)

        self.play = Gtk.Button(label="▶️")
        self.play.add_css_class("circular")
        self.play.set_valign(Gtk.Align.CENTER)
        self.play.set_size_request(50,50)
        self.play.connect("clicked", self.onPlay)
        self.is_playing = False

        self.next = Gtk.Button(label="⏭️")
        self.next.add_css_class("circular")
        self.next.set_valign(Gtk.Align.CENTER)
        self.next.connect("clicked", self.onNext)

        self.folderButton = Gtk.Button(label="Select a Folder")
        self.folderButton.connect("clicked", self.onFolderButton)


        # ---------------------------------------------- #
        self.songBox.append(self.artwork)
        self.songBox.append(self.song)

        self.controlsBox.append(self.previous)
        self.controlsBox.append(self.play)
        self.controlsBox.append(self.next)

        mainBox.append(self.songBox)
        mainBox.append(self.controlsBox)
        mainBox.append(self.folderButton)

        
        toolbar_view.set_content(mainBox)
        win.set_content(toolbar_view)
        
        self.main_window = win
        win.present()

    def update_track(self, index):
        track = self.tracks[index]
        self.artwork_image.set_paintable(track.artwork)

        if self.is_playing:
            self.song.set_label(f"{track.title} - {track.artist}")
            player = Player(track.path)
            player.play()
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

        dialog.select_folder(self.main_window, None, self.onFolderSelected)
    def onFolderSelected(self, dialog, result):
        try:
            folder = dialog.select_folder_finish(result)
            self.getTracks(folder.get_path())
            self.update_track(self.current_track_index)
        except gi.repository.GLib.Error:
            pass
    
    def getTracks(self, path: Path):
        library = Library(path)
        tracks = library.getTracks()

        for track in tracks:
            song = Song(track)
            self.tracks.append(song)

app = MyApp()
app.run(None)
