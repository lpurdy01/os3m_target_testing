import tkinter as tk
from pywinusb import hid
from collections import deque

# Set your VID and PID here
VID = 0x0483
PID = 0x572b

# Check if the device is connected
def is_device_connected(vid, pid):
    target_filter = hid.HidDeviceFilter(vendor_id=vid, product_id=pid)
    devices = target_filter.get_devices()
    return len(devices) > 0

# Initialize the HID device
def init_hid_device(vid, pid):
    target_filter = hid.HidDeviceFilter(vendor_id=vid, product_id=pid)
    devices = target_filter.get_devices()
    if devices:
        device = devices[0]
        device.open()
        return device
    else:
        return None

class JoystickApp(tk.Tk):
    def __init__(self, hid_device):
        super().__init__()
        self.hid_device = hid_device
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
        for i, dat in enumerate(data):
            canvas, bar = self.axis_bars[i]
            new_width = (dat[-1] / FINE + 1) * 100
            canvas.coords(bar, 0, 0, new_width, 20)
            print(f"Axis {i}: {dat[-1]}")  # Print the axis status to the terminal
        self.after(100, self.update_ui)

    def on_closing(self):
        if self.hid_device:
            self.hid_device.close()
        self.destroy()

# Setup deques to store the data for plotting
buffer_size = 50  # Reduced buffer size for UI responsiveness
data = [deque([0] * buffer_size, maxlen=buffer_size) for _ in range(6)]
FINE = 50  # Set range of view

def handle_data(data_packet):
    values = [int.from_bytes(data_packet[i * 2 + 1:i * 2 + 3], byteorder='little', signed=True) for i in range(6)]
    for val, dat in zip(values, data):
        dat.append(val)

if __name__ == "__main__":
    if is_device_connected(VID, PID):
        hid_device = init_hid_device(VID, PID)
        if hid_device:
            hid_device.set_raw_data_handler(handle_data)
            app = JoystickApp(hid_device)
            app.protocol("WM_DELETE_WINDOW", app.on_closing)
            app.mainloop()
        else:
            print("Failed to initialize the HID device.")
    else:
        print("HID device not connected.")
