# Python AR.Drone 2.0
#
# Copyright (C) 2013 Quadeare <lacrampe.florian@gmail.com>
# Twitter : @quadeare

import sys
from pygame import *  
import pygame
import libardrone
import threading
import time
#import cv
from subprocess import call
import numpy as np

import signal 



class video(threading.Thread):
    """Video class to launch media flux"""
    def __init__(self, nom = ''):
        threading.Thread.__init__(self)
        self.process = None
    def run(self):
        print "Video"
        call(["ffplay", "http://192.168.1.1:5555/"])
    def stop(self):
        call(["killall", "ffplay"])
        if self.process is not None:
            self.process.terminate()
            self.process = None

class controle(threading.Thread):
    """Control class (to control the drone)"""
    def __init__(self, nom = ''):
        threading.Thread.__init__(self)
        self._stopevent = threading.Event( )
    def stop(self):
        self._stopevent.set( )
    def run(self):
    
        """We call pygame (to use controler)"""
        pygame.init()

        """Launch drone class"""
        drone = libardrone.ARDrone(True)
        clock = pygame.time.Clock()
        running = True

        """Set up and init joystick"""
        #j=joystick.Joystick(0) 
        #j.init()

        tookoff = False

        speed = 1

        while running:
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    key = pygame.key.get_pressed() 
                    # takeoff/land
                    if key[pygame.K_SPACE]:
                        if (tookoff):
                            print "Land !"
                            drone.land()
                            tookoff = False
                        else:
                            print "Take Off !"
                            drone.takeoff()
                            tookoff = True

                    # End
                    elif key[pygame.K_BACKSPACE]:
                        print "End !"
                        if (tookoff):
                            drone.land()
                            time.sleep(2)
                        running = False

                    # Altitude UP
                    elif key[pygame.K_w]:
                        print "Altitude UP"
                        drone.speed = speed
                        drone.move_up()

                    # Altitude Down
                    elif key[pygame.K_s]:
                        print "Altitude Down"
                        drone.speed = speed
                        drone.move_down()

                    # Left
                    elif key[pygame.K_LEFT]:
                        print "Left !"
                        drone.speed = speed
                        drone.move_left()

                    # Right
                    elif key[pygame.K_RIGHT]:
                        print "Right !"
                        drone.speed = speed
                        drone.move_right()
                        
                    # Forward
                    elif key[pygame.K_UP]:
                        print "Forward !"
                        drone.speed = speed
                        drone.move_forward()

                    # Reverse
                    elif key[pygame.K_DOWN]:
                        print "Reverse !"
                        drone.speed = speed
                        drone.move_backward()
                        
                    # Turn left
                    elif key[pygame.K_a]:
                        print "Turn left !"
                        drone.speed = speed
                        drone.turn_left()

                    # Turn right
                    elif key[pygame.K_d]:
                        print "Turn right !"
                        drone.speed = speed
                        drone.turn_right()
                        
                    # Emmergency
                    elif key[pygame.K_RETURN]:
                        print "Emergency !"
                        drone.reset()
                        
                    # Anim : Boom !
                    elif key[pygame.K_p]:
                        print "Anim : Boom !"
                        drone.event_boom()
                        
                    # Anim : Turnarround !
                    elif key[pygame.K_f]:
                        print "Anim : Turnarround !"
                        drone.event_turnarround()  

                    # Anim : Yaw Shake !
                    elif key[pygame.K_l]:
                        print "Anim : Yaw Shake !"
                        drone.event_yawshake()
                        
                    # Anim : Yaw Dance !
                    elif key[pygame.K_m]:
                        print "Anim : Yaw Dance !"
                        drone.event_yawdance()
                        
                    # Anim : ThetaMixed !
                    elif key[pygame.K_o]:
                        print "Anim : ThetaMixed !"
                        drone.event_thetamixed()

                    # Set speed 0.1
                    elif key[pygame.K_1]:
                        print "Set : Speed 1 !"
                        speed = 0.1

                    # Set speed 0.2
                    elif key[pygame.K_2]:
                        print "Set : Speed 2 !"
                        speed = 0.2

                    # Set speed 0.3
                    elif key[pygame.K_3]:
                        print "Set : Speed 3 !"
                        speed = 0.3

                    # Set speed 0.4
                    elif key[pygame.K_4]:
                        print "Set : Speed 4 !"
                        speed = 0.4

                    # Set speed 0.5
                    elif key[pygame.K_5]:
                        print "Set : Speed 5 !"
                        speed = 0.5

                    # Set speed 0.6
                    elif key[pygame.K_6]:
                        print "Set : Speed 6 !"
                        speed = 0.6

                    # Set speed 0.7
                    elif key[pygame.K_7]:
                        print "Set : Speed 7 !"
                        speed = 0.7

                    # Set speed 0.8
                    elif key[pygame.K_8]:
                        print "Set : Speed 8 !"
                        speed = 0.8

                    # Set speed 0.9
                    elif key[pygame.K_9]:
                        print "Set : Speed 9 !"
                        speed = 0.9

                    # Set speed 1
                    elif key[pygame.K_0]:
                        print "Set : Speed 10 !"
                        speed = 1


                if event.type == pygame.KEYUP:
                    # Altitude UP
                    if key[pygame.K_w] or key[pygame.K_a] or key[pygame.K_s] or key[pygame.K_d] or key[pygame.K_UP] or key[pygame.K_DOWN] or key[pygame.K_LEFT] or key[pygame.K_RIGHT]:
                        print "STOP !"
                        drone.speed = 0
                        drone.hover()
                    
                            
            clock.tick(10000)
        print "Shutting down...",
        drone.reset()
        drone.halt()
        print "Ok."

    
if __name__ == '__main__':
    try:

        # Video
        video = video('Thread Video')
        video.start()


        # Controler
        controle = controle('Thread Controler')
        controle.run()

        video.stop()
        quit()
    except (KeyboardInterrupt, SystemExit):
        cleanup_stop_thread();
        video.stop()
        sys.exit()
