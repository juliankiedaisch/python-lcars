# -*- coding: iso-8859-1 -*-
from Tkinter import *
import tkFont, time
from threading import Thread, Lock
from Objects.button import StandardButton
from Objects.elements import *
from Objects.core import Modul

class KalenderGui:
    def __init__(self, root, core, width=1200, height=800, background="black"):
        self.__root = root
        self.core = core
        self.__width= width
        self.__height = height
        self.__background = background
        self.__lock = Lock()
        self.__position = 105
        self.__lauferObj = []
        self.__headfont = tkFont.Font(family="LCARSGTJ3", size=36)
        self.__headcolor = "#FFFFFF"
        self.__objfarbe = "#006699"
        self.__objfarbe2 = "#ccddbb"
        self.__canvas = Canvas(root, width=width, height=height, background=background)
        self.__canvas.pack()
        self.__zeit = None
        self.__zeitObj = None
        self.__build()    