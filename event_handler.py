# Function for handling events
class EventHandler:

    def __init__(self):
        self.mouse_down = False

    def on_mouse_down(self):
        self.mouse_down = not self.mouse_down