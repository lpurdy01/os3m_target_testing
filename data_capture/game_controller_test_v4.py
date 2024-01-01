import tkinter as tk
from threading import Thread
from inputs import get_gamepad

class GameControllerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Game Controller Axes")

        self.axis_count = 6  # Adjusted for 6 axes
        self.axis_values = [0] * self.axis_count
        self.axis_bars = []

        # Create UI elements for each axis
        for i in range(self.axis_count):
            label = tk.Label(root, text=f"Axis {i}:")
            label.grid(row=i, column=0)

            canvas = tk.Canvas(root, width=200, height=20)
            canvas.grid(row=i, column=1)
            bar = canvas.create_rectangle(0, 0, 100, 20, fill="blue")
            self.axis_bars.append((canvas, bar))

        # Start the thread for reading controller inputs
        self.running = True
        self.thread = Thread(target=self.update_axes)
        self.thread.start()

    def update_axes(self):
        while self.running:
            events = get_gamepad()
            for event in events:
                if event.ev_type == 'Absolute':
                    axis_index = self.map_axis(event.code)
                    if axis_index is not None and axis_index < self.axis_count:
                        self.axis_values[axis_index] = (event.state + 32768) / 65536
                        self.update_ui()

            self.root.update()

    def map_axis(self, axis_code):
        # Map the axis code to an index
        axis_mapping = {
            'ABS_X': 0,
            'ABS_Y': 1,
            'ABS_Z': 2,
            'ABS_RX': 3,
            'ABS_RY': 4,
            'ABS_RZ': 5
        }
        return axis_mapping.get(axis_code)

    def update_ui(self):
        for i, value in enumerate(self.axis_values):
            canvas, bar = self.axis_bars[i]
            new_width = value * 200  # Convert from 0:1 to 0:200 range
            canvas.coords(bar, 0, 0, new_width, 20)

    def on_closing(self):
        self.running = False
        self.root.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    app = GameControllerApp(root)
    root.protocol("WM_DELETE_WINDOW", app.on_closing)
    root.mainloop()
