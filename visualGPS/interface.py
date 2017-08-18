from asciimatics.widgets import Layout, Frame, Divider, Button, ListBox, Label
from asciimatics.screen import Screen
from asciimatics.scene import Scene
from asciimatics.exceptions import ResizeScreenError, NextScene
from collections import defaultdict
import sys

last_scene = None

class HeaderView(Frame):
    def __init__(self, screen, gps_controller):
        super(HeaderView, self).__init__(screen, screen.height * 2 // 3, screen.width * 2 // 3, title="Visual GPS")
        self.gps_controller = gps_controller
        self.layout = Layout([100], fill_frame=True)
        self.add_layout(self.layout)
        self.header_height = len(self.gps_controller.reader.header_structure)

        self.message_enum = self.gps_controller.parser.current_frame["message_enum"]
        self.payload_data = self.gps_controller.parser.current_frame["payload_data"]

        self.header_label = Label("Frame Header")

        self.header_list = ListBox(self.header_height, self._convert_dict_to_options(self.gps_controller.reader.header_structure))
        self.header_list.disabled = True

        self.payload_list = ListBox(1, [(self.message_enum, 0)])
        self.payload_list.disabled = True

        self.frame_count_list = ListBox(1, [(str(self.gps_controller.parser.frame_count), 0)])
        self.frame_count_list.disabled = True

        self.payload_data = ListBox(len(self.payload_data), self._convert_dict_to_options(self.payload_data))
        self.payload_data.disabled = True

        self.layout.add_widget(self.header_label)
        self.layout.add_widget(Divider())
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

        self.palette = defaultdict(
            lambda: (Screen.COLOUR_WHITE, Screen.A_NORMAL, Screen.COLOUR_BLACK)
        )
        self.palette["focus_button"] = (Screen.COLOUR_BLACK, Screen.A_BOLD, Screen.COLOUR_WHITE)

    def _next_frame(self):
        self.gps_controller.get_frame()
        self.header_list.options = self._convert_dict_to_options(self.gps_controller.reader.header_structure)
        self.payload_list.options = [(self.gps_controller.parser.current_frame["message_enum"], 0)]
        self.frame_count_list.options = [(str(self.gps_controller.parser.frame_count), 0)]
        self.payload_data.options = self._convert_dict_to_options(self.gps_controller.parser.current_frame["payload_data"])

    def _convert_dict_to_options(self, dict):
        options = [(field[0] + " : " + str(field[1]), count) for count, field in enumerate(dict.items())]

        return options

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
