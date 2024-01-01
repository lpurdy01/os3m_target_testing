import matplotlib.pyplot as plt
import matplotlib.animation as animation
from collections import deque
from pywinusb import hid

# Set range of view
FINE = 50
COURSE = 2048

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
buffer_size = 500  # Assuming 100 updates per second, 500 samples would be 5 seconds
data = [deque([0] * buffer_size, maxlen=buffer_size) for _ in range(6)]

# Create a new figure for the plot
fig, ax = plt.subplots()

# The lines to be plotted
lines = [ax.plot(dat, label=f'Value {i + 1}')[0] for i, dat in enumerate(data)]

# Set the y-axis limits
ax.set_ylim(-FINE, FINE)
# ax.set_ylim(-COURSE, COURSE)

# Add this line to show the grid
ax.grid(True)

# ax.legend(0)


def handle_data(data_packet):
    # The first byte is the report ID and not a data value, ignore it
    values = [int.from_bytes(data_packet[i * 2 + 1:i * 2 + 3], byteorder='little', signed=True) for i in range(6)]

    # Add new data to the deques
    for val, dat in zip(values, data):
        dat.append(val)


# Register a callback to handle incoming data
hid_device.set_raw_data_handler(handle_data)


def update(frame):
    # Update the plots
    for line, dat in zip(lines, data):
        line.set_ydata(dat)


ani = animation.FuncAnimation(fig, update, interval=10)  # 100 updates per second

plt.show()

# At the end close the device
hid_device.close()