# MIT License
#
# Copyright (c) 2020 Russ Hughes
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

import time
import random
import machine
import st7789py
import uos

def pick_item(sequence):
    div = 0x3fffffff // len(sequence)
    return sequence[random.getrandbits(30) // div]


def draw(display, message, start_x=0, start_y=32, color=0, font_file="/fonts/romant.fnt"):
    '''
    Draw message on the OLED display at the given location in specified
    font.

    Args:
        message (str): The message to write
        start_x (int): column to start at, defaults to 0
        start_y int): row to start at, defaults to 32
        font_file (str): The Hershy font file to use, defaults to romant.fnt

    '''
    from_x = to_x = pos_x = start_x
    from_y = to_y = pos_y = start_y
    penup = True

    with open(font_file, "rb", buffering=0) as file:
        characters = int.from_bytes(file.read(2), 'little')
        if characters > 96:
            begins = 0x00
            ends = characters
        else:
            begins = 0x20
            ends = characters + 0x20

        for char in [ord(char) for char in message]:
            if begins <= char <= ends:
                file.seek((char-begins+1)*2)
                file.seek(int.from_bytes(file.read(2), 'little'))
                length = ord(file.read(1))
                left, right = file.read(2)

                left -= 0x52            # Position left side of the glyph
                right -= 0x52           # Position right side of the glyph
                width = right - left    # Calculate the character width

                for vect in range(length):
                    vector_x, vector_y = file.read(2)
                    vector_x -= 0x52
                    vector_y -= 0x52

                    if vector_x == -50:
                        penup = True
                        continue

                    if not vect or penup:
                        from_x = pos_x + vector_x - left
                        from_y = pos_y + vector_y

                    else:
                        to_x = pos_x + vector_x - left
                        to_y = pos_y + vector_y

                        display.line(from_x, from_y, to_x, to_y, color)

                        from_x = to_x
                        from_y = to_y

                    penup = False

                pos_x += width


bl = machine.Pin(4, machine.Pin.OUT)
bl.value(1)

spi = machine.SPI(
    2,
    baudrate=30000000,
    polarity=1,
    phase=1,
    sck=machine.Pin(18),
    mosi=machine.Pin(19))

display = st7789py.ST7789(
    spi, 135, 240,
    reset=machine.Pin(23, machine.Pin.OUT),
    cs=machine.Pin(5, machine.Pin.OUT),
    dc=machine.Pin(16, machine.Pin.OUT))

display.init()
display.fill(st7789py.BLACK)

fonts = ["astrol.fnt", "cyrilc.fnt", "gotheng.fnt", "gothger.fnt",
         "gothita.fnt", "greeks.fnt", "italicc.fnt", "italiccs.fnt",
         "italiccs.fnt", "meteo.fnt", "music.fnt", "romanc.fnt",
         "romancs.fnt", "romand.fnt", "romanp.fnt", "romans.fnt",
         "romant.fnt", "scriptc.fnt", "scripts.fnt"]

line = 0
while True:
    color = st7789py.color565(
        random.getrandbits(8),
        random.getrandbits(8),
        random.getrandbits(8))

    line += 32

    font_file = "/fonts/" + pick_item(fonts)
    print (font_file)
    draw(display, "Hello!", 0, line, color, font_file)

    if line > 192:
        display.fill(st7789py.BLACK)
        line = 0
