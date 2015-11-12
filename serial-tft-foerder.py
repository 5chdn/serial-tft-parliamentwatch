# display parliamentwatch number of supporters on serial tft display
# for the raspberry pi rev1 with the hobbytronics 1.8 inch lcd.
#
# code is released under public domain using wtfpl v2.
# written 2015 by @5chdn <schoedon@abgeordnetenwatch.de>
#
# requires python2, python2-pyserial
# requires serialtft: https://github.com/Gadgetoid/Serial-TFT-Python

import sys, os
import time, datetime
from time import strftime, strptime
sys.path.append(os.path.abspath("/path/to/serial-tft-python"))
from serialtft import SerialTFT

# setup the serialtft library, we dont want to clean up the lcd on exit
# so specify false for clear_on_exit. we're not sure whether we are driving
# the serialtft within sane limits, so we will turn on flush.
#
# serialtft( device, baud_rate, clear_on_exit, flush )
tft = SerialTFT("/dev/ttyAMA0", 9600, False, True)

# read supporter count from file
# kindly ask support for API access (ref ticket #AW-3028)
count_file = "/path/to/counter"
modified_time = 0
supporter_count = "Err0"
try:
  dump = open(count_file)
  supporter_count = str(dump.read())
  modified_time = int(os.path.getmtime(count_file))
  modified_time = datetime.datetime.fromtimestamp(modified_time)
  modified_time = modified_time.strftime("%d.%m.%Y %H:%M:%S")
except IOError:
  print "Oops! Could not read file."
  supporter_count = "Err1"
except ValueError:
  print "Oops! Could not convert value(s)."
  supporter_count = "Err2"
except:
  print "Oops! Unknown error."
  supporter_count = "Err3"

# initialize and clear the screen
tft.screen_rotation(SerialTFT.Rotation.landscape)
tft.bg_color(SerialTFT.Color.black)
tft.clear_screen()

# write organization title
tft.font_size(SerialTFT.Font.small)
tft.fg_color(SerialTFT.Color.yellow)
tft.goto_pixel(SerialTFT.Screen.width_half-51,5)
tft.write("Abgeordnetenwatch")
tft.goto_pixel(SerialTFT.Screen.width_half-33,15)
tft.write("hat aktuell")

# write huge number of supporters
tft.font_size(SerialTFT.Font.large)
tft.fg_color(SerialTFT.Color.red)
tft.goto_pixel(SerialTFT.Screen.width_half-32,SerialTFT.Screen.height_half-22)
tft.write(supporter_count)

# write supporter subline
tft.font_size(SerialTFT.Font.small)
tft.fg_color(SerialTFT.Color.yellow)
tft.goto_pixel(SerialTFT.Screen.width_half-51,SerialTFT.Screen.height_half+13)
tft.write("Foerdermitglieder")

# write bottom line with timestamp
tft.font_size(SerialTFT.Font.small)
tft.fg_color(SerialTFT.Color.green)
tft.goto_pixel(SerialTFT.Screen.width_half-45,SerialTFT.Screen.height-19)
tft.write("Letztes Update:")
tft.goto_pixel(SerialTFT.Screen.width_half-54,SerialTFT.Screen.height-10)
tft.write(modified_time)
