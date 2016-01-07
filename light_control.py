#!/usr/bin/env python
##udp_client.py
from  socket import *
from Adafruit_PWM_Servo_Driver import PWM
import time


HOST = ''
PORT = 10000
ADDR = (HOST,PORT)
BUFSIZE = 64

pwm = PWM (0x40, debug=False)
pwm.setPWMFreq (400)
udp_recv_client = socket( AF_INET,SOCK_DGRAM)
udp_recv_client.setsockopt (SOL_SOCKET, SO_REUSEADDR, 1)
udp_recv_client.bind (ADDR)

current_channel = CHANNEL_RED

CHANNEL_RED   = 0
CHANNEL_GREEN = 1
CHANNEL_BLUE  = 2

current_red_pwm   = 4095
current_green_pwm = 4095
current_blue_pwm  = 4095


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
    
    ramp_pwm (CHANNEL_RED,   current_red_pwm,   end_red_val,   2)
    ramp_pwm (CHANNEL_GREEN, current_green_pwm, end_green_val, 2)
    ramp_pwm (CHANNEL_BLUE,  current_blue_pwm,  end_blue_val,  2)


    current_red_pwm   = end_red_val
    current_green_pwm = end_green_val
    current_blue_pwm  = end_blue_val
    
def init ():
    
    lamp_A_status = 0
    lamp_B_status = 0
    lamp_C_status = 0

    pwm.setPWM (3, 0, lamp_A_status * 4095)
    pwm.setPWM (4, 0, lamp_B_status * 4095)
    pwm.setPWM (5, 0, lamp_C_status * 4095)
    

while True:

    init ()
    
#    print "Waiting to receive"
    time.sleep (0.5)
    data = udp_recv_client.recv(BUFSIZE)
    print data
    
    if (data == "Page_Up"):
        lamp_A_status = 1 - lamp_A_status
        pwm.setPWM (0, 0, lamp_A_status * 4095)

    elif (data == "Next"):
        lamp_A_status = 1 - lamp_B_status
        pwm.setPWM (1, 0, lamp_B_status * 4095)

    elif (data == "slash"):
        lamp_C_status = 1 - lamp_C_status
        pwm.setPWM (2, 0, lamp_C_status * 4095)

    elif (data == "Up"):
        set_three_channels (current_red_pwm + 409, current_green_pwm, current_blue_pwm)

    elif (data == "Down"):
        set_three_channels (current_red_pwm - 409, current_green_pwm, current_blue_pwm)

    elif (data == "Right"):
        set_three_channels (current_red_pwm, current_green_pwm + 409, current_blue_pwm)

    elif (data == "Left"):
        set_three_channels (current_red_pwm, current_green_pwm - 409, current_blue_pwm)

    elif (data == "B"):
        set_three_channels (current_red_pwm, current_green_pwm, current_blue_pwm + 409)

    elif (data == "B"):
        set_three_channels (current_red_pwm, current_green_pwm, current_blue_pwm + 409)


cli.close()
