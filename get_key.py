#!/usr/bin/env python
# get_key.py
"""
A simple example of hooking the keyboard on Linux using pyxhook
"""

#Libraries we need
import pyxhook
import time
from   socket      import *

udp_send_sock = socket(AF_INET, SOCK_DGRAM)
UDP_SEND_ADDRESS = ('', 10000)
#This function is called every time a key is presssed
def kbevent( event ):
    #print key info
    print event
    
    udp_send_sock.sendto (event.Key, UDP_SEND_ADDRESS)
    #If the ascii value matches spacebar, terminate the while loop
    #if event.Ascii == 32:
    #    global running
    #    running = False

#Create hookmanager
hookman = pyxhook.HookManager()
#Define our callback to fire when a key is pressed down
hookman.KeyDown = kbevent
#Hook the keyboard
hookman.HookKeyboard()
#Start our listener
hookman.start()
    
#Create a loop to keep the application running
running = True
while running:
    time.sleep(0.1)

#Close the listener when we are done
hookman.cancel()