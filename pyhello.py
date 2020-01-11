import sys
import time
import machine
import st7789
import uos
import random

sys.path.append('/pyfonts')
import pytext
import romans
import scriptc

bl = machine.Pin(4, machine.Pin.OUT)
bl.value(1)

spi = machine.SPI(
    2,
    baudrate=30000000,
    polarity=1,
    phase=1,
    sck=machine.Pin(18),
    mosi=machine.Pin(19))

display = st7789.ST7789(
    spi, 135, 240,
    reset=machine.Pin(23, machine.Pin.OUT),
    cs=machine.Pin(5, machine.Pin.OUT),
    dc=machine.Pin(16, machine.Pin.OUT))

display.init()
display.fill(st7789.BLACK)

row = 0
again = True
while again:
    color = st7789.color565(
        random.getrandbits(8),
        random.getrandbits(8),
        random.getrandbits(8))

    row += 32

    if (row % 64 == 0):
        pytext.text(display, scriptc, "Hello!", row, 0, color)
    else:
        pytext.text(display, romans, "Hello!", row, 0, color)

    if row > 192:
        display.fill(st7789.BLACK)
        row = 0
