import csv
import serial
import threading
from datetime import datetime
from pywinusb import hid

# HID Device Setup
VID = 0x0483
PID = 0x572b

# Serial Port Setup
SERIAL_PORT = 'COM7'
SERIAL_BAUDRATE = 115200

# Shared variable for HID data
latest_hid_values = [0] * 6
hid_data_lock = threading.Lock()

# Test Run Name
test_run_name = input("Enter test run name: ")

# File Setup
filename = test_run_name + datetime.now().strftime('%Y%m%dT%H%M%S') + '.csv'

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
    global latest_hid_values
    with hid_data_lock:
        latest_hid_values = [int.from_bytes(data_packet[i * 2 + 1:i * 2 + 3], byteorder='little', signed=True) for i in range(6)]

# HID data processing thread
def hid_thread():
    hid_device = init_hid_device(VID, PID)
    if hid_device:
        hid_device.set_raw_data_handler(handle_data)
        while True:
            pass  # Keep the thread alive
    if hid_device:
        hid_device.close()

# Start the HID thread
threading.Thread(target=hid_thread, daemon=True).start()

# Initialize serial port
ser = serial.Serial(SERIAL_PORT, SERIAL_BAUDRATE, timeout=1)

# Main loop
try:
    with open(filename, 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["Timestamp", "Reading", "Unit", "LDC_Val_2", "LDC_Val_1"])

        while True:
            line = ser.readline().decode('utf-8').strip()
            if line:
                number, unit = line.split()
                with hid_data_lock:
                    ldc_val_2 = latest_hid_values[0]  # Use the first HID value
                    ldc_val_1 = latest_hid_values[1]  # Use the second HID value
                writer.writerow([datetime.now(), number, unit, ldc_val_2, ldc_val_1])
                print(f"Logged: {datetime.now()}, {number}, {unit}, {ldc_val_2}, {ldc_val_1}")
except KeyboardInterrupt:
    print("Script terminated by user.")
finally:
    if ser.is_open:
        ser.close()
