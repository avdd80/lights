#!/usr/bin/env python
##udp_client.py
from  socket import *
import time
import RPi.GPIO as GPIO

HOST = ''
PORT = 10000
ADDR = (HOST,PORT)
BUFSIZE = 128

lamp_A_gpio = 16
lamp_B_gpio = 20
lamp_C_gpio = 19 # unused

udp_recv_client = socket( AF_INET,SOCK_DGRAM)
udp_recv_client.setsockopt (SOL_SOCKET, SO_REUSEADDR, 1)
udp_recv_client.bind (ADDR)


lamp_A_status = 0
lamp_B_status = 0
lamp_C_status = 0

def init ():
    
    # Pin Setup:
    GPIO.setmode(GPIO.BCM) # Broadcom pin-numbering scheme
    GPIO.setup(lamp_A_gpio, GPIO.OUT) # pin set as output
    GPIO.setup(lamp_B_gpio, GPIO.OUT) # pin set as output
    GPIO.setup(lamp_C_gpio, GPIO.OUT) # pin set as output - unused in hardware

def turn_on_lamp_A ():
    GPIO.output(lamp_A_gpio, GPIO.HIGH)

def turn_on_lamp_B ():
    GPIO.output(lamp_B_gpio, GPIO.HIGH)
    
# Unused
def turn_on_lamp_C ():
    GPIO.output(lamp_C_gpio, GPIO.HIGH)

def turn_off_lamp_A ():
    GPIO.output(lamp_A_gpio, GPIO.LOW)

def turn_off_lamp_B ():
    GPIO.output(lamp_B_gpio, GPIO.LOW)

# Unused
def turn_off_lamp_C ():
    GPIO.output(lamp_C_gpio, GPIO.LOW)

while True:

    init ()
    
#    print "Waiting to receive"
    time.sleep (0.5)
    data = udp_recv_client.recv(BUFSIZE)
    print data

    elif (data == "space"):
        # If all are off, turn them on
        if (lamp_A_status and lamp_B_status and lamp_C_status):
            lamp_A_status = 0
            lamp_B_status = 0
            lamp_C_status = 0
        else:        
            lamp_A_status = 1
            lamp_B_status = 1
            lamp_C_status = 1


cli.close ()
