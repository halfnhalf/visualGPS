from asciimatics.widgets import Layout, Frame, Divider, Button, ListBox, Label, Widget
from asciimatics.screen import Screen
from asciimatics.exceptions import NextScene
from asciimatics.renderers import BarChart
from asciimatics.effects import Print
from asciimatics.renderers import BarChart
from collections import defaultdict

import time

last_scene = None

class _GraphView(Frame):
    def __init__(self, screen, gps_controller):
        super(_GraphView, self).__init__(screen, screen.height * 2 // 3, screen.width * 2 // 3, title="Visual GPS")
        self.gps_controller = gps_controller
        self.layout = Layout([100], fill_frame=True)
        self.add_layout(self.layout)
        self.screen = screen

        self.header_label = Label("Graph")
        self.layout.add_widget(Button("Back", self._go_to_frame_window))

        self.fix()

        self.palette = defaultdict(
            lambda: (Screen.COLOUR_WHITE, Screen.A_NORMAL, Screen.COLOUR_BLACK)
        )
        self.palette["focus_button"] = (Screen.COLOUR_BLACK, Screen.A_BOLD, Screen.COLOUR_WHITE)

    def _go_to_frame_window(self):
        raise NextScene("Frame")
        pass

    def _convert_dict_to_options(self, dict):
        options = [(field[0] + " : " + str(field[1]), count) for count, field in enumerate(dict.items())]

        return options

def build_graph_view(screen, gps_controller):
    effects = [
        _GraphView(screen, gps_controller),
        Print(screen,
              BarChart(
                  7, 60, [lambda: time.time() * 10 % 101],
                  gradient=[
                      (33, Screen.COLOUR_RED, Screen.COLOUR_RED),
                      (66, Screen.COLOUR_YELLOW, Screen.COLOUR_YELLOW),
                      (100, Screen.COLOUR_WHITE, Screen.COLOUR_WHITE),
                  ] if screen.colours < 256 else [
                      (10, 234, 234), (20, 236, 236), (30, 238, 238),
                      (40, 240, 240), (50, 242, 242), (60, 244, 244),
                      (70, 246, 246), (80, 248, 248), (90, 250, 250),
                      (100, 252, 252)
                  ],
                  char=">",
                  scale=100.0,
                  labels=True,
                  axes=BarChart.X_AXIS),
              x=68, y=16, transparent=False, speed=2)
    ]
    return effects
