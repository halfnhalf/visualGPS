from asciimatics.widgets import Layout, Frame, Label, Widget, Divider, Button, ListBox
from asciimatics.screen import Screen
from asciimatics.scene import Scene
from asciimatics.exceptions import ResizeScreenError, NextScene
import sys

last_scene = None

class HeaderView(Frame):
    def __init__(self, screen, gps_controller):
        super(HeaderView, self).__init__(screen, screen.height * 2 // 3, screen.width * 2 // 3, title="Header Information")

        self.gps_controller = gps_controller
        self.layout = Layout([100], fill_frame=True)
        self.add_layout(self.layout)
        self.header_list = ListBox(Widget.FILL_FRAME,
                                   self._convert_dict_to_options(self.gps_controller.reader.header_structure))
        self.layout.add_widget(self.header_list)
        self.layout.add_widget(Button("next frame", self._next_frame))
        self.fix()

    def _next_frame(self):
        self.gps_controller.get_frame()
        self.header_list.options = self._convert_dict_to_options(self.gps_controller.reader.header_structure)

    def _convert_dict_to_options(self, dict):
        list_items = dict.items()
        list_items_string = [(str(field), count) for count, field in enumerate(list_items)]
        return list_items_string



def build_header_view(screen, scene, gps_controller):
    scenes = [
        Scene([HeaderView(screen, gps_controller)], -1, name="Header")
    ]
    screen.play(scenes, start_scene=scene)


def start_tui(gps_controller):
    global last_scene
    while True:
        try:
            Screen.wrapper(build_header_view, arguments=[last_scene, gps_controller])
            sys.exit(0)
        except ResizeScreenError as e:
            last_scene = e.scene
