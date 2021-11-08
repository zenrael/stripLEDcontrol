import time, getopt, sys
from rpi_ws281x import *

# RIGHT HAND SIDE IS STRIP 1

RIGHT_LED_COUNT = 35
RIGHT_LED_PIN = 12
RIGHT_LED_FREQ_HZ = 800000
RIGHT_LED_DMA = 10
RIGHT_LED_BRIGHTNESS = 255
RIGHT_LED_INVERT = False
RIGHT_LED_CHANNEL = 0

LEFT_LED_COUNT = 48
LEFT_LED_PIN = 13 # 13 IS CHANNEL 1
LEFT_LED_FREQ_HZ = 800000
LEFT_LED_DMA = 10
LEFT_LED_BRIGHTNESS = 255
LEFT_LED_INVERT = False
LEFT_LED_CHANNEL = 1

presets = {'PEGGY_PURPLE': Color(30,0,255),
            'HPS_LAMP': Color(255,70,0) }

def SetSolid(color, strip):
    for i in range(strip.numPixels()):
        strip.setPixelColor(i, color)
        strip.show()
        time.sleep(50/1000.0)

def SetSolidAll(color, strip_1, strip_2):
    for i in range(max(strip_1.numPixels(), strip_2.numPixels())):
        if i < strip_1.numPixels():
            strip_1.setPixelColor(i, color)
            strip_1.show()
        if i < strip_2.numPixels():
            strip_2.setPixelColor(i, color)
            strip_2.show()
        time.sleep(50/1000.0)

def Pulse(color, strip, pulse_width):
    # First get the number of LED's in the strip
    led_num = strip.numPixels()
    # We know this is divided approx into 3
    led_per_bar = int(led_num/3)
    # Then pulse!
    for i in range(int(led_per_bar)):
        strip.setPixelColor(i, color)
        strip.setPixelColor(2*led_per_bar-i, color)
        strip.setPixelColor(i+(2*led_per_bar), color)
        strip.show()
        time.sleep(pulse_width/1000.0)
    # Quickly get the stragglers at the end...
    for i in range(int(3*led_per_bar), led_num, 1):
        strip.setPixelColor(i, color)
    strip.show()
    # Now bring it back down with a lovely -ve range...
    # First kill the stragglers...
    for i in range(int(3*led_per_bar), led_num, 1):
        strip.setPixelColor(i, Color(0,0,0))
    strip.show()
    for i in range(int(led_per_bar),0,-1):
        strip.setPixelColor(i, Color(0,0,0))
        strip.setPixelColor(2*led_per_bar-i, Color(0,0,0))
        strip.setPixelColor(i+(2*led_per_bar), Color(0,0,0))
        strip.show()
        time.sleep(pulse_width/1000.0)
    # There are 'end stragglers' this time...
    for i in range(led_num):
        strip.setPixelColor(i, Color(0,0,0))
    strip.show()

def Blackout(strip):
    for i in range(strip.numPixels()):
        strip.setPixelColor(i, Color(0,0,0))
        strip.show()

def main(options,args):
    print('Press Ctrl-C to quit.')

    strip_left = Adafruit_NeoPixel(LEFT_LED_COUNT, LEFT_LED_PIN, LEFT_LED_FREQ_HZ, LEFT_LED_DMA, LEFT_LED_INVERT, LEFT_LED_BRIGHTNESS, LEFT_LED_CHANNEL)
    strip_right = Adafruit_NeoPixel(RIGHT_LED_COUNT, RIGHT_LED_PIN, RIGHT_LED_FREQ_HZ, RIGHT_LED_DMA, RIGHT_LED_INVERT, RIGHT_LED_BRIGHTNESS, RIGHT_LED_CHANNEL)

    strip_left.begin()
    strip_right.begin()

    Blackout(strip_right)
    Blackout(strip_left)

    for opt, arg in options:
        if opt == '-p':
            SetSolidAll(presets[arg], strip_right, strip_left)
        if opt == '-P':
            arg_list = arg.split(':')
            p_width = int(arg_list[1])
            val_list = arg_list.split(',')
            vals = list(map(int, val_list))
            Pulse(Color(vals[0], vals[1], vals[2]), strip_right, p_width)
        if opt == '-s':
            arg_list = arg.split(',')
            vals = list(map(int, arg_list))
            SetSolidAll(Color(vals[0],vals[1],vals[2]), strip_right, strip_left)


if __name__ == '__main__':
    try:
        options, args = getopt.getopt(sys.argv[1:], "s:p:P:")
    except getopt.GetoptError:
        print('usage: stripLEDcontrol.py -s R,G,B\n'
              '       stripLEDcontrol.py -p PRESET\n'
              'PRESETS: PEGGY_PURPLE, HPS_LAMP\n')
        sys.exit(2)
    main(options,args)