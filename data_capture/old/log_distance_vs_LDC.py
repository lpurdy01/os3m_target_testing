import csv
import serial
import tkinter as tk
from pywinusb import hid
from collections import deque
from datetime import datetime

# HID Device Setup
VID = 0x0483  # Set your HID device's Vendor ID
PID = 0x572b  # Set your HID device's Product ID

# Serial Port Setup
SERIAL_PORT = 'COM7'
SERIAL_BAUDRATE = 115200

# File Setup
filename = datetime.now().strftime('%Y%m%dT%H%M%S') + '.csv'

# Function to initialize HID device
def init_hid_device(vid, pid):
    target_filter = hid.HidDeviceFilter(vendor_id=vid, product_id=pid)
    devices = target_filter.get_devices()
    if devices:
        device = devices[0]
        device.open()
        return device
    else:
        return None

# Function to handle HID data
def handle_data(data_packet):
    values = [int.from_bytes(data_packet[i * 2 + 1:i * 2 + 3], byteorder='little', signed=True) for i in range(6)]
    # Write to CSV: time, dist, dist_unit, ldc_val
    with open(filename, 'a', newline='') as file:
        writer = csv.writer(file)
        # Assuming the first LDC value is what you need
        ldc_val = values[0]
        # Read a line from the serial port
        line = ser.readline().decode('utf-8').strip()
        if line:
            number, unit = line.split()
            writer.writerow([datetime.now(), number, unit, ldc_val])
            print(f"Logged: {datetime.now()}, {number}, {unit}, {ldc_val}")

# Initialize serial port
ser = serial.Serial(SERIAL_PORT, SERIAL_BAUDRATE, timeout=1)

# Initialize HID device
hid_device = init_hid_device(VID, PID)
if hid_device:
    hid_device.set_raw_data_handler(handle_data)

# Write CSV header
with open(filename, 'w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(["Timestamp", "Reading", "Unit", "LDC_Val"])

# Main loop
try:
    while True:
        pass  # Keep the script running
except KeyboardInterrupt:
    print("Script terminated by user.")
finally:
    if hid_device:
        hid_device.close()
    if ser.is_open:
        ser.close()
