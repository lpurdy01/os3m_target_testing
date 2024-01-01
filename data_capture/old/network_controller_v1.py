import pygame
import socket
import json
import time

dead_zone = 0.15

def get_controller_input():
    pygame.init()
    pygame.joystick.init()
    joystick = pygame.joystick.Joystick(0)
    joystick.init()

    while True:
        pygame.event.pump()
        axis_x = joystick.get_axis(0)  # Adjust the axis as needed
        axis_y = joystick.get_axis(1)
        axis_z = joystick.get_axis(5)-joystick.get_axis(4)

        if abs(axis_x) < dead_zone:
            axis_x = 0
        if abs(axis_y) < dead_zone:
            axis_y = 0
        if abs(axis_z) < dead_zone:
            axis_z = 0
        yield axis_x, axis_y, axis_z

def broadcast_data(host, port, data):
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
        s.sendto(json.dumps(data).encode('utf-8'), (host, port))

def main():
    host, port = 'localhost', 12345  # Address for broadcasting
    for axis_x, axis_y, axis_z in get_controller_input():
        broadcast_data(host, port, {'x': axis_x, 'y': axis_y, 'z': axis_z})
        print({'x': axis_x, 'y': axis_y, 'z': axis_z})
        time.sleep(0.02)  # Adjust frequency of updates as needed

if __name__ == "__main__":
    main()
