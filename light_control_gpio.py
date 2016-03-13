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

def set_lamp_A (status):
    if (status == 1):
        GPIO.output(lamp_A_gpio, GPIO.HIGH)
    elif (status == 0):
        GPIO.output(lamp_A_gpio, GPIO.LOW)

def set_lamp_B (status):
    if (status == 1):
        GPIO.output(lamp_B_gpio, GPIO.HIGH)
    elif (status == 0):
        GPIO.output(lamp_B_gpio, GPIO.LOW)

def set_lamp_C (status):
    if (status == 1):
        GPIO.output(lamp_C_gpio, GPIO.HIGH)
    elif (status == 0):
        GPIO.output(lamp_C_gpio, GPIO.LOW)

try:
    while True:

        init ()
    
#    print "Waiting to receive"
        time.sleep (0.5)
        data = udp_recv_client.recv(BUFSIZE)
        print data

        if (data == "space"):
            # If all are off, turn them on
            if (not (lamp_A_status or lamp_B_status or lamp_C_status)):
                lamp_A_status = 1
                lamp_B_status = 1
                lamp_C_status = 1
            else:        
                lamp_A_status = 0
                lamp_B_status = 0
                lamp_C_status = 0
            
        if (data == "a" or data == "A"):
            lamp_A_staus = 1
        

        set_lamp_A (lamp_A_status)
        set_lamp_B (lamp_B_status)
        set_lamp_C (lamp_C_status)
    except KeyboardInterrupt:
        GPIO.cleanup ()


cli.close ()
