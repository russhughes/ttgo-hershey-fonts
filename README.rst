ttgo-lcd-demo
=============

MicroPython Hershey fonts demo for the TTGO-LCD using the st7789py_mpy driver
from https://github.com/devbis/st7789py_mpy


I pulled this from the oledui module I wrote for my `TurtlePlotBot
<https://github.com/russhughes/TurtlePlotBot>`_ it's not fast but it works
and should be easy to modify to run on most any board and display.


Copy the hello.py to the MicroPython device then create a /fonts directory
and copy all the fnt files into it.  I use `mpfshell
<https://github.com/wendlers/mpfshell>`_ for this. Then import hello and
enjoy.
