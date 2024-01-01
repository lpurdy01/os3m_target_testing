import csv
import serial
from datetime import datetime

# Open the serial port.
ser = serial.Serial('COM7', 115200, timeout=1)

# Get the current time in ISO8601 format and use it as the filename.
filename = datetime.now().strftime('%Y%m%dT%H%M%S') + '.csv'

# Open the CSV file in append mode.
with open(filename, 'a', newline='') as file:
    writer = csv.writer(file)
    # Write the header if the file is empty.
    if file.tell() == 0:
        writer.writerow(["Timestamp", "Reading", "Unit"])

    # Loop forever.
    while True:
        # Read a line from the serial port.
        line = ser.readline().decode('utf-8').strip()
        # If the line was not empty, write it to the CSV file with a timestamp.
        if line:
            print(f'Received: {line}')  # Print the received data to the terminal.
            # Split the line into number and unit.
            number, unit = line.split()
            writer.writerow([datetime.now(), number, unit])
            file.flush()  # Ensure the line is written immediately.