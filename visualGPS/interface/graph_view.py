from asciimatics.widgets import Layout, Frame, Divider, Button, ListBox, Label, Widget
from asciimatics.screen import Screen
from asciimatics.exceptions import NextScene
from collections import defaultdict

last_scene = None

class GraphView(Frame):
    def __init__(self, screen, gps_controller):
        super(GraphView, self).__init__(screen, screen.height * 2 // 3, screen.width * 2 // 3, title="Visual GPS")
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
