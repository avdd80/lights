#!/usr/bin/env python
## light_control.py
from  socket import *
from Adafruit_PWM_Servo_Driver import PWM
import time
import RPi.GPIO as GPIO


HOST = ''
PORT = 10000
ADDR = (HOST,PORT)
BUFSIZE = 128

pwm = PWM (0x40, debug=False)
pwm.setPWMFreq (400)

lamp_A_gpio = 16
lamp_B_gpio = 20
lamp_C_gpio = 19 # unused

udp_recv_client = socket( AF_INET,SOCK_DGRAM)
udp_recv_client.setsockopt (SOL_SOCKET, SO_REUSEADDR, 1)
udp_recv_client.bind (ADDR)

CHANNEL_RED   = 0
CHANNEL_GREEN = 1
CHANNEL_BLUE  = 2

current_red_pwm   = 4095
current_green_pwm = 4095
current_blue_pwm  = 4095

lamp_A_status = 0
lamp_B_status = 0
lamp_C_status = 0

# This function ramps up/down the PWM at a specified rate on a
# specified channel. The second argument is the start PWM value
# that approaches the third argument as it is ramped up/down
def ramp_pwm (channel, start_val, end_val, rate):
    
    # The rate at which the PWM duty cycle is changed. Here, rate
    # is approximately expressed in percentage
    PWM_STEP_SIZE = rate * 40
    
    # Time period between two PWM duty changes
    PWM_STEP_PERIOD = 0.05 # 50 milliseconds

    if (start_val < end_val):
        while ((start_val < end_val) and (start_val < 4096)):
            pwm.setPWM (channel, 0, 4095 - start_val)
            time.sleep (PWM_STEP_PERIOD)
            start_val = start_val + PWM_STEP_SIZE

    else:
        while ((start_val >= end_val) and (start_val >= 0)):
            pwm.setPWM (channel, 0, 4095 - start_val)
            time.sleep (PWM_STEP_PERIOD)
            start_val = start_val - PWM_STEP_SIZE

    # Adjust the correct PWM end value
    pwm.setPWM (channel, 0, 4095 - end_val)

def set_three_channels (end_red_val, end_green_val, end_blue_val):
    
    global current_red_pwm
    global current_green_pwm
    global current_blue_pwm
    
    ramp_pwm (CHANNEL_RED,   current_red_pwm,   end_red_val,   2)
    ramp_pwm (CHANNEL_GREEN, current_green_pwm, end_green_val, 2)
    ramp_pwm (CHANNEL_BLUE,  current_blue_pwm,  end_blue_val,  2)


    current_red_pwm   = end_red_val
    current_green_pwm = end_green_val
    current_blue_pwm  = end_blue_val
    
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
        time.sleep (0.2)
        data = udp_recv_client.recv(BUFSIZE)
        print data
    
        if (data == "Page_Up"):
            # Turn all on
            lamp_A_status = 1
            lamp_B_status = 1
            lamp_C_status = 1

        elif (data == "Next"):
            # Turn all off
            lamp_A_status = 0
            lamp_B_status = 0
            lamp_C_status = 0
            
        # Toggle all lamps
        elif (data =="space"):
            lamp_A_status = 1 - lamp_A_status
            lamp_B_status = 1 - lamp_B_status
            lamp_C_status = 1 - lamp_C_status

        elif (data == "a" or data == "A" or data == "[269025046]"):
            lamp_A_status = 1
        elif (data == "q" or data == "Q" or data == "[269025047]"):
            lamp_A_status = 0
        elif (data == "Left" or data == "b" or data == "B"):
            lamp_B_status = 1
        elif (data == "Right" or data == "g" or data == "G"):
            lamp_B_status = 0
        elif (data == "c" or data == "C" or data == "[269025044]"):
            lamp_C_status = 1
        elif (data == "d" or data == "D" or data == "[269025045]"):
            lamp_C_status = 0

        elif (data == "Up"):
            set_three_channels (current_red_pwm + 409, current_green_pwm, current_blue_pwm)

        elif (data == "Down"):
            set_three_channels (current_red_pwm - 409, current_green_pwm, current_blue_pwm)

        elif (data == "Right"):
            set_three_channels (current_red_pwm, current_green_pwm + 409, current_blue_pwm)

        elif (data == "Left"):
            set_three_channels (current_red_pwm, current_green_pwm - 409, current_blue_pwm)

        elif (data == "[269025043]"):
            set_three_channels (current_red_pwm, current_green_pwm, current_blue_pwm + 409)

        elif (data == "[269025041]"):
            set_three_channels (current_red_pwm, current_green_pwm, current_blue_pwm + 409)

        set_lamp_A (lamp_A_status)
        set_lamp_B (lamp_B_status)
        set_lamp_C (lamp_C_status)
except KeyboardInterrupt:
        GPIO.cleanup ()


cli.close()
