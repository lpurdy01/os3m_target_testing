import tkinter as tk
from pywinusb import hid
from collections import deque

# Set range of view
FINE = 50
# COURSE = 2048

# Set your VID and PID here
VID = 0x0483
PID = 0x572b

# Create a filter for the target HID device
target_filter = hid.HidDeviceFilter(vendor_id=VID, product_id=PID)

# Get the first device matching the filter
hid_device = target_filter.get_devices()[0]

# Open the device
hid_device.open()

# Setup deques to store the data for plotting
buffer_size = 50  # Reduced buffer size for UI responsiveness
data = [deque([0] * buffer_size, maxlen=buffer_size) for _ in range(6)]

class JoystickApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Joystick Axes")

        self.axis_bars = []
        for i in range(6):
            label = tk.Label(self, text=f"Axis {i}:")
            label.grid(row=i, column=0)

            canvas = tk.Canvas(self, width=200, height=20)
            canvas.grid(row=i, column=1)
            bar = canvas.create_rectangle(0, 0, 100, 20, fill="blue")
            self.axis_bars.append((canvas, bar))

        self.after(100, self.update_ui)

    def update_ui(self):
        # Update the UI with the latest data
        for i, dat in enumerate(data):
            canvas, bar = self.axis_bars[i]
            # Assume the data is scaled between -FINE and FINE
            new_width = (dat[-1] / FINE + 1) * 100
            canvas.coords(bar, 0, 0, new_width, 20)
        self.after(100, self.update_ui)

def handle_data(data_packet):
    # The first byte is the report ID and not a data value, ignore it
    values = [int.from_bytes(data_packet[i * 2 + 1:i * 2 + 3], byteorder='little', signed=True) for i in range(6)]

    # Add new data to the deques
    for val, dat in zip(values, data):
        dat.append(val)

# Register a callback to handle incoming data
hid_device.set_raw_data_handler(handle_data)

# Start the tkinter app
app = JoystickApp()
app.mainloop()

# At the end, close the device
hid_device.close()
