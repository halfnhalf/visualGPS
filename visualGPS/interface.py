from asciimatics.widgets import Layout, Frame, Label
from asciimatics.screen import Screen
from asciimatics.scene import Scene
from asciimatics.exceptions import ResizeScreenError
import sys


class HeaderView(Frame):
    def __init__(self, screen):
        super(HeaderView, self).__init__(screen, screen.height * 2 // 3, screen.width * 2 // 3, title="Header Information")
        layout = Layout([100], fill_frame=True)
        self.add_layout(layout)
        layout.add_widget(Label("Place Holder:Place Holder:Place Holder:Place Holder:Place Holder:Place Holder:"))
        self.fix()


def build_header_view(screen):
    scenes = [
        Scene([HeaderView(screen)], -1, name="Header")
    ]
    screen.play(scenes)


def start_tui():
    while True:
        try:
            Screen.wrapper(build_header_view)
            sys.exit(0)
        except ResizeScreenError:
            pass
