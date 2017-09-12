from asciimatics.screen import Screen
from asciimatics.exceptions import ResizeScreenError, NextScene
from asciimatics.scene import Scene
from visualGPS.interface.frame_view import FrameView
from visualGPS.interface.graph_view import GraphView 

last_scene = None

def start_tui(gps_controller):
    global last_scene
    while True:
        try:
            Screen.wrapper(_build_view, arguments=[last_scene, gps_controller])
            sys.exit(0)
        except ResizeScreenError as e:
            last_scene = e.scene

def _build_view(screen, scene, gps_controller):
    scenes = [
        Scene([FrameView(screen, gps_controller)], -1, name="Frame"),
        Scene([GraphView(screen, gps_controller)], -1, name="Graph")
    ]
    screen.play(scenes, start_scene=scene)
