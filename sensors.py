#!/usr/bin/env python3

import sys
from grove.factory import Factory
import math
from grove.adc import ADC
import time
from gpiozero import Buzzer
from grove.button import Button
import smbus
import RPi.GPIO as GPIO
 
#Code temperature 

def temperature():
 
    sensor = Factory.getTemper("NTC-ADC", 0)
 
    temp = sensor.temperature

    return temp
 
 
#Code sound

class GroveSoundSensor:
 
    def __init__(self, channel):
        self.channel = channel
        self.adc = ADC()
 
    @property
    def sound(self):
        value = self.adc.read(self.channel)
        return value
 
Grove = GroveSoundSensor
 
 
def sound():
    sensor = GroveSoundSensor(2)
 
    sound = sensor.sound

    return sound
 
#code Gas 
 
class GroveGasSensorMQ2:
 
    def __init__(self, channel):
        self.channel = channel
        self.adc = ADC()
 
    @property
    def MQ2(self):
        value = self.adc.read(self.channel)
        return value
 
Grove = GroveGasSensorMQ2
 
 
def gas_main():
    sensor = GroveGasSensorMQ2(4)

    gas = sensor.MQ2

    return gas

# code Buzzer 

def sound_alert(state):
    buzzer = Buzzer(5)
    if state == 1:
        buzzer.on()
        time.sleep(0.1)
    else:
        buzzer.off()
    

# code LCD

bus = smbus.SMBus(1)

# this device has two I2C addresses
DISPLAY_RGB_ADDR = 0x62
DISPLAY_TEXT_ADDR = 0x3e
 
def setRGB(r,g,b):
    bus.write_byte_data(DISPLAY_RGB_ADDR,0,0)
    bus.write_byte_data(DISPLAY_RGB_ADDR,1,0)
    bus.write_byte_data(DISPLAY_RGB_ADDR,0x08,0xaa)
    bus.write_byte_data(DISPLAY_RGB_ADDR,4,r)
    bus.write_byte_data(DISPLAY_RGB_ADDR,3,g)
    bus.write_byte_data(DISPLAY_RGB_ADDR,2,b)
 
def textCommand(cmd):
    bus.write_byte_data(DISPLAY_TEXT_ADDR,0x80,cmd)

def setText_norefresh(text):
    textCommand(0x02) # return home
    time.sleep(.05)
    textCommand(0x08 | 0x04) # display on, no cursor
    textCommand(0x28) # 2 lines
    time.sleep(.05)
    count = 0
    row = 0
    while len(text) < 32: #clears the rest of the screen
        text += ' '
    for c in text:
        if c == '\n' or count == 16:
            count = 0
            row += 1
            if row == 2:
                break
            textCommand(0xc0)
            if c == '\n':
                continue
        count += 1
        bus.write_byte_data(DISPLAY_TEXT_ADDR,0x40,ord(c))

def print_on_lcd(text, type):
    setText_norefresh(text)
    if type == 'error':
        setRGB(255, 0, 0)
    elif type == 'message':
        setRGB(0, 0, 255)
    elif type == 'normal':
        setRGB(0, 255, 0)

# code bouton


class GroveButton(object):
    def __init__(self, pin):
        # High = pressed
        self.state = False
        self.__btn = Factory.getButton("GPIO-HIGH", pin)
        self.__last_time = time.time()
        self.__on_press = None
        self.__on_release = None
        self.__btn.on_event(self, GroveButton.__handle_event)
 
    @property
    def on_press(self):
        return self.__on_press
 
    @on_press.setter
    def on_press(self, callback):
        if not callable(callback):
            return
        self.__on_press = callback
 
    @property
    def on_release(self):
        return self.__on_release
 
    @on_release.setter
    def on_release(self, callback):
        if not callable(callback):
            return
        self.__on_release = callback
 
    def __handle_event(self, evt):
        dt, self.__last_time = evt["time"] - self.__last_time, evt["time"]
        if evt["code"] == Button.EV_LEVEL_CHANGED:
            if evt["pressed"]:
                if callable(self.__on_press):
                    self.__on_press(dt)
            else:
                if callable(self.__on_release):
                    self.__on_release(dt)
 
 
Grove = GroveButton
 
pin = 12
 
button = GroveButton(pin)

def on_press(t):
    button.state = True

def on_release(t):
    button.state = False
 
button.on_press = on_press
button.on_release = on_release
