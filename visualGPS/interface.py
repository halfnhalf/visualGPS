from asciimatics.widgets import Layout, Frame, Label, Widget, Divider, Button, ListBox
from asciimatics.screen import Screen
from asciimatics.scene import Scene
from asciimatics.exceptions import ResizeScreenError, NextScene
import sys

last_scene = None

class HeaderView(Frame):
    def __init__(self, screen, gps_controller):
        super(HeaderView, self).__init__(screen, screen.height * 2 // 3, screen.width * 2 // 3, title="Visual GPS")

        self.gps_controller = gps_controller
        header_height = len(self.gps_controller.reader.header_structure)
        self.layout = Layout([100], fill_frame=True)
        self.add_layout(self.layout)
        self.header_list = ListBox(header_height,
                                   self._convert_dict_to_options(self.gps_controller.reader.header_structure))
        self.payload_list = ListBox(1,
                                    [(self.gps_controller.parser.message_enum, 0)])
        self.frame_count_list = ListBox(1,
                                         [(str(self.gps_controller.parser.frame_count), 0)])
        self.payload_data = ListBox(1,
                                         [(str(self.gps_controller.parser.payload_data["#ofobservers"]), 0)])
        self.layout.add_widget(self.header_list)
        self.layout.add_widget(Divider())
        self.layout.add_widget(self.payload_list)
        self.layout.add_widget(Divider())
        self.layout.add_widget(self.frame_count_list)
        self.layout.add_widget(Divider())
        self.layout.add_widget(self.payload_data)
        self.layout.add_widget(Divider())
        self.layout.add_widget(Button("next frame", self._next_frame))
        self.fix()

    def _next_frame(self):
        self.gps_controller.get_frame()
        self.header_list.options = self._convert_dict_to_options(self.gps_controller.reader.header_structure)
        self.payload_list.options = [(self.gps_controller.parser.message_enum, 0)]
        self.frame_count_list.options = [(str(self.gps_controller.parser.frame_count), 0)]
        self.payload_data.options = [(str(self.gps_controller.parser.payload_data["#ofobservers"]), 0)]

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
