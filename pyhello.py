import sys
import time
import machine
import st7789
import uos
import random

sys.path.append('/pyfonts')
import astrol
import cyrilc
import gotheng
#import gothger
#import gothita
import greeks
import italicc
import italiccs
import meteo
import music
import romanc
import romancs
import romand
import romanp
import romans
import romant
import scriptc
import scripts

import pytext

fonts = [astrol, cyrilc, gotheng, greeks, italicc, italiccs,
         italiccs, meteo, music, romanc,
         romancs, romand, romanp, romans,
         romant, scriptc, scripts]



def pick_item(sequence):
    div = 0x3fffffff // len(sequence)
    return sequence[random.getrandbits(30) // div]

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

    pytext.text(display, pick_item(fonts), "Hello!", row, 0, color)

    if row > 192:
        display.fill(st7789.BLACK)
        row = 0
