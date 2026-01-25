
import sys
import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk
from .ui.main_window import MiruMainWindow

def main():
    app = MiruMainWindow()
    app.connect("destroy", Gtk.main_quit)
    app.show_all()
    Gtk.main()

if __name__ == "__main__":
    main()
