import pygame

def init():
    pygame.init()
    pygame.joystick.init()
    joystick = pygame.joystick.Joystick(0)  # Assumes you have at least one controller connected
    joystick.init()
    print(f"Initialized joystick: {joystick.get_name()}")
    return joystick

def main():
    joystick = init()

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.JOYAXISMOTION:
                axis_id = event.axis
                axis_value = joystick.get_axis(axis_id)
                print(f"Axis {axis_id} moved to {axis_value:.2f}")

if __name__ == "__main__":
    main()
