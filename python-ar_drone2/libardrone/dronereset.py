
import libardrone

import signal
import sys
import time
import signal


running = True

drone = libardrone.ARDrone(True)


drone.reset()
drone.halt()
quit()
