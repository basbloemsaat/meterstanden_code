#!/usr/bin/env python

# script leest de meter uit en voegt het toe aan de csv van vandaag. Als bestand nog niet bestaat maakt hij het aan

import re
import serial
from slimme_meter import SlimmeMeterData
import sys
from pprint import pprint

# Set COM port config
ser = serial.Serial()
ser.baudrate = 115200
ser.bytesize = serial.SEVENBITS
ser.parity = serial.PARITY_EVEN
ser.stopbits = serial.STOPBITS_ONE
ser.xonxoff = 0
ser.rtscts = 0
ser.timeout = 20
ser.port = "/dev/ttyUSB0"

# Open COM port
try:
    ser.open()
except:
    sys.exit("Fout bij het openen van %s." % ser.name)

doloop = True
res = SlimmeMeterData()

while doloop:
    p1_line = ''
    try:
        p1_raw = ser.readline()
    except:
        sys.exit("Seriele poort %s kan niet gelezen worden." % ser.name)

    p1_str = p1_raw.decode('UTF-8')
    p1_line = p1_str.strip()

    if re.match('^!', p1_line):
        doloop = False
        break

    # pprint(p1_line)
    res.add_raw_line(p1_line)




# Close port and show status
try:
    ser.close()
except:
    sys.exit("Kon de seriele poort %s niet sluiten." % ser.name)

# pprint(res.data)

res.save_to_csv()

# # doe iets met res (vertalen en aan csv appenden)

# line = slimme_meter.raw_to_csv_line(res)
# pprint(line)


