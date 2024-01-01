import tkinter as tk
import pygame
from threading import Thread

class GameControllerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Game Controller Axes")

        # Initialize pygame for controller input
        pygame.init()
        pygame.joystick.init()
        self.joystick = pygame.joystick.Joystick(0)
        self.joystick.init()

        self.axis_count = self.joystick.get_numaxes()
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
            pygame.event.pump()
            for i in range(self.axis_count):
                axis_value = self.joystick.get_axis(i)
                canvas, bar = self.axis_bars[i]
                new_width = (axis_value + 1) * 100  # Convert from -1:1 to 0:200 range
                canvas.coords(bar, 0, 0, new_width, 20)
            self.root.update()

    def on_closing(self):
        self.running = False
        self.root.destroy()
        pygame.quit()

if __name__ == "__main__":
    root = tk.Tk()
    app = GameControllerApp(root)
    root.protocol("WM_DELETE_WINDOW", app.on_closing)
    root.mainloop()
