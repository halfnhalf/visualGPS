from asciimatics.widgets import Layout, Frame, Divider, Button, ListBox, Label, Widget
from asciimatics.screen import Screen
from asciimatics.exceptions import NextScene
from collections import defaultdict
import sys
import _thread
import time

last_scene = None

class FrameView(Frame):
    def __init__(self, screen, gps_controller):
        super(FrameView, self).__init__(screen, screen.height * 2 // 3, screen.width * 2 // 3, title="Visual GPS")
        self.gps_controller = gps_controller
        self.layout = Layout([100], fill_frame=True)
        self.add_layout(self.layout)
        self.header_height = len(self.gps_controller.reader.header_structure)
        self.screen = screen

        self.message_enum = self.gps_controller.parser.current_frame["message_enum"]
        self.payload_data = self.gps_controller.parser.current_frame["payload_data"]

        self.header_label = Label("Frame Header")

        self.header_list = ListBox(self.header_height, self._convert_dict_to_options(self.gps_controller.reader.header_structure))
        self.header_list.disabled = True

        self.payload_list = ListBox(1, [(self.message_enum, 0)])
        self.payload_list.disabled = True

        self.frame_count_list = ListBox(1, [(str(self.gps_controller.parser.frame_count), 0)])
        self.frame_count_list.disabled = True

        self.payload_data = ListBox(Widget.FILL_FRAME, self._convert_dict_to_options(self.payload_data))
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
        self.layout.add_widget(Button("Start", self._start_real_time))
        self.layout.add_widget(Button("Graph", self._go_to_graph))
        self.fix()

        self.palette = defaultdict(
            lambda: (Screen.COLOUR_WHITE, Screen.A_NORMAL, Screen.COLOUR_BLACK)
        )
        self.palette["focus_button"] = (Screen.COLOUR_BLACK, Screen.A_BOLD, Screen.COLOUR_WHITE)
    
    def _go_to_graph(self):
        raise NextScene("Graph")

    def _next_frame(self):
        self.gps_controller.get_frame()
        self.header_list.options = self._convert_dict_to_options(self.gps_controller.reader.header_structure)
        self.payload_list.options = [(self.gps_controller.parser.current_frame["message_enum"], 0)]
        self.frame_count_list.options = [(str(self.gps_controller.parser.frame_count), 0)]
        self.payload_data.options = self._convert_dict_to_options(self.gps_controller.parser.current_frame["payload_data"])

    def _start_real_time(self):
        _thread.start_new_thread(self._real_time, ())

    def _real_time(self):
        while(True):
            self.gps_controller.get_frame()
            self.header_list.options = self._convert_dict_to_options(self.gps_controller.reader.header_structure)
            self.payload_list.options = [(self.gps_controller.parser.current_frame["message_enum"], 0)]
            self.frame_count_list.options = [(str(self.gps_controller.parser.frame_count), 0)]
            self.payload_data.options = self._convert_dict_to_options(self.gps_controller.parser.current_frame["payload_data"])
            self.screen.force_update()

    def _convert_dict_to_options(self, dict):
        options = [(field[0] + " : " + str(field[1]), count) for count, field in enumerate(dict.items())]

        return options
