
import libardrone

from pygame import *
import pygame
import signal
import sys
import time
import signal

pygame.init()
#clock = pygame.time.Clock()

running = True

drone = libardrone.ARDrone(True)


# Failsafe
def signal_handler(signal, frame):
    drone.land()
    time.sleep(2)
    drone.reset()
    drone.halt()
    quit()



signal.signal(signal.SIGINT, signal_handler)

time.sleep(1)

drone.takeoff()
time.sleep(3)
drone.hover()
time.sleep(2)


'''
# Move 2 meters forward
drone.speed = libardrone.hormps2dps(2) # 2 mps
drone.move_forward()
time.sleep(1.6)
drone.hover()
time.sleep (2)

# Move 2 meters left
drone.speed = libardrone.hormps2dps(2) # 2 mps
drone.move_left()
time.sleep(1.6)
drone.hover()
time.sleep (2)

# Move 2 meters backward
drone.speed = libardrone.hormps2dps(2) # 2 mps
drone.move_backward()
time.sleep(1.6)
drone.hover()
time.sleep (2)

# Move 2 meters right
drone.speed = libardrone.hormps2dps(2) # 2 mps
drone.move_right()
time.sleep(1.6)
drone.hover()
time.sleep (2)
'''


# Move 2 meters forward
drone.speed = libardrone.hormps2dps(2) # 2 mps
drone.move_forward()
time.sleep(2.6)
drone.hover()
time.sleep (2)

# Move 2 meters forward
drone.speed = libardrone.rps2dps(0.25) # 2 mps
drone.turn_left()
time.sleep(2)
drone.hover()
time.sleep (2)

# Move 2 meters forward
drone.speed = libardrone.hormps2dps(2) # 2 mps
drone.move_forward()
time.sleep(2.6)
drone.hover()
time.sleep (2)

# Move 2 meters forward
drone.speed = libardrone.rps2dps(0.25) # 2 mps
drone.turn_left()
time.sleep(2)
drone.hover()
time.sleep (2)

# Move 2 meters forward
drone.speed = libardrone.hormps2dps(2) # 2 mps
drone.move_forward()
time.sleep(2.6)
drone.hover()
time.sleep (2)

# Move 2 meters forward
drone.speed = libardrone.rps2dps(0.25) # 2 mps
drone.turn_left()
time.sleep(2)
drone.hover()
time.sleep (2)

'''
# Turn around once
drone.speed = libardrone.rps2dps(0.25) # 0.25 rps
drone.turn_left()
time.sleep(4)
drone.hover()
time.sleep (1)

# Go up 1 meter
drone.speed = libardrone.verumps2dps(1) # 1 mps
drone.move_up()
time.sleep(1)
drone.hover()
time.sleep (1)

# Go down 1 meter
drone.speed = libardrone.verdmps2dps(1) # 1 mps
drone.move_down()
time.sleep(1)
drone.hover()
time.sleep (2)
'''

drone.land()
time.sleep(3)
drone.reset()
drone.halt()
quit()
