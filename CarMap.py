#-*- coding:UTF-8 -*-
import RPi.GPIO as GPIO
import time
#!/usr/bin/env python

import glob
import os
import time
from sys import exit


#小车电机引脚定义
IN1 = 20
IN2 = 21
IN3 = 19
IN4 = 26
ENA = 16
ENB = 13

#设置GPIO口为BCM编码方式
GPIO.setmode(GPIO.BCM)

#忽略警告信息
GPIO.setwarnings(False)

#电机引脚初始化操作
def motor_init():
    global pwm_ENA
    global pwm_ENB
    global delaytime
    GPIO.setup(ENA,GPIO.OUT,initial=GPIO.HIGH)
    GPIO.setup(IN1,GPIO.OUT,initial=GPIO.LOW)
    GPIO.setup(IN2,GPIO.OUT,initial=GPIO.LOW)
    GPIO.setup(ENB,GPIO.OUT,initial=GPIO.HIGH)
    GPIO.setup(IN3,GPIO.OUT,initial=GPIO.LOW)
    GPIO.setup(IN4,GPIO.OUT,initial=GPIO.LOW)
    #设置pwm引脚和频率为2000hz
    pwm_ENA = GPIO.PWM(ENA, 2000)
    pwm_ENB = GPIO.PWM(ENB, 2000)
    pwm_ENA.start(0)
    pwm_ENB.start(0)

#小车前进   
def run(delaytime):
    GPIO.output(IN1, GPIO.HIGH)
    GPIO.output(IN2, GPIO.LOW)
    GPIO.output(IN3, GPIO.HIGH)
    GPIO.output(IN4, GPIO.LOW)
    pwm_ENA.ChangeDutyCycle(80)
    pwm_ENB.ChangeDutyCycle(80)
    time.sleep(delaytime)

#小车后退
def back(delaytime):
    GPIO.output(IN1, GPIO.LOW)
    GPIO.output(IN2, GPIO.HIGH)
    GPIO.output(IN3, GPIO.LOW)
    GPIO.output(IN4, GPIO.HIGH)
    pwm_ENA.ChangeDutyCycle(80)
    pwm_ENB.ChangeDutyCycle(80)
    time.sleep(delaytime)

#小车左转   
def left(delaytime):
    GPIO.output(IN1, GPIO.LOW)
    GPIO.output(IN2, GPIO.LOW)
    GPIO.output(IN3, GPIO.HIGH)
    GPIO.output(IN4, GPIO.LOW)
    pwm_ENA.ChangeDutyCycle(80)
    pwm_ENB.ChangeDutyCycle(80)
    time.sleep(delaytime)

#小车右转
def right(delaytime):
    GPIO.output(IN1, GPIO.HIGH)
    GPIO.output(IN2, GPIO.LOW)
    GPIO.output(IN3, GPIO.LOW)
    GPIO.output(IN4, GPIO.LOW)
    pwm_ENA.ChangeDutyCycle(80)
    pwm_ENB.ChangeDutyCycle(80)
    time.sleep(delaytime)

#小车原地左转
def spin_left(delaytime):
    GPIO.output(IN1, GPIO.LOW)
    GPIO.output(IN2, GPIO.HIGH)
    GPIO.output(IN3, GPIO.HIGH)
    GPIO.output(IN4, GPIO.LOW)
    pwm_ENA.ChangeDutyCycle(80)
    pwm_ENB.ChangeDutyCycle(80)
    time.sleep(delaytime)

#小车原地右转
def spin_right(delaytime):
    GPIO.output(IN1, GPIO.HIGH)
    GPIO.output(IN2, GPIO.LOW)
    GPIO.output(IN3, GPIO.LOW)
    GPIO.output(IN4, GPIO.HIGH)
    pwm_ENA.ChangeDutyCycle(80)
    pwm_ENB.ChangeDutyCycle(80)
    time.sleep(delaytime)

#小车停止   
def brake(delaytime):
    GPIO.output(IN1, GPIO.LOW)
    GPIO.output(IN2, GPIO.LOW)
    GPIO.output(IN3, GPIO.LOW)
    GPIO.output(IN4, GPIO.LOW)
    pwm_ENA.ChangeDutyCycle(80)
    pwm_ENB.ChangeDutyCycle(80)
    time.sleep(delaytime)
    
try:
    import pygame
except ImportError:
    exit("This script requires the pygame module\nInstall with: sudo pip install pygame")

import drumhat


DRUM_FOLDER = "drums2"

print("""This example lets you play the drums with Drum HAT and move using the motor HAT!

Pads are mapped like so:

7 = Rim hit, 1 = Whistle - foward , 2 = Clash
6 = Hat - left,     8 = Clap - back,   3 = Cowbell - right
      5 = Snare,   4 = Base

Press CTRL+C to exit!
""")

BANK = os.path.join(os.path.dirname(__file__), DRUM_FOLDER)

pygame.mixer.init(44100, -16, 1, 512)
pygame.mixer.set_num_channels(16)

files = glob.glob(os.path.join(BANK, "*.wav"))
files.sort()

samples = [pygame.mixer.Sound(f) for f in files]

def handle_hit(event):
    # event.channel is a zero based channel index for each pad
    # event.pad is the pad number from 1 to 8
    samples[event.channel].play(loops=0)
    print("You hit pad {}, playing: {}".format(event.pad,files[event.channel]))
    if event.pad == 1:
            run(.5)
            brake(.5)
    elif event.pad == 8:
            back(.5)
            brake(.5)
    elif event.pad == 3:
            right(.5)
            brake(.5)
    elif event.pad == 6:
            left(.5)
            brake(.5)
    
            
    

def handle_release():
    pass


#延时2s   
time.sleep(2)

#try/except语句用来检测try语句块中的错误，
#从而让except语句捕获异常信息并处理。
#小车循环前进1s，后退1s，左转2s，右转2s，原地左转3s
#原地右转3s，停止1s。


userin = 0
#userin = input("Press a command to use the car. Type q to leave.")

if userin != quit:
    motor_init()

while userin != "quit": 
    try:
        drumhat.on_hit(drumhat.PADS, handle_hit)
        drumhat.on_release(drumhat.PADS, handle_release)    
        #hile True:
        #    run(1)
        #fo
        #back(1)
        #left(2)
        #right(2)
        #spin_left(3)
        #spin_right(3)
        #brake(1)
    except KeyboardInterrupt:
        pass
    #userin = input("Press a command to use the car. Type q to leave.")

pwm_ENA.stop()
pwm_ENB.stop()
GPIO.cleanup() 

