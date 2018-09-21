# -*- coding: iso-8859-1 -*-
from Tkinter import *
import tkFont, time
from colour import Color
from threading import Thread, Lock

class Button(Canvas):
    def __init__(self, root, width=120, height=50, background="black", font=["LCARSGTJ3", "16"], schalter=False):
        self.width = width
        self.height = height
        self.root = root
        self.background = background
        self.state = 1
        self.__schalter = schalter
        self.bgElements = []
        self.textElements = []
        self.bgElementsColor = [Color("#ccccff"), Color("#99ccff"), Color("#ff9900")]
        self.textElementsColor = [Color("#CCCCCC"), Color("#000000"), Color("#000000")]
        self.exFunction = None
        self.exFunctionParams = None
        self.__lock = Lock()
        self.font = tkFont.Font(family=font[0], size=font[1])
        Canvas.__init__(self,self.root, width=self.width,height=self.height, background=self.background,  bd=0, highlightthickness=0, relief='ridge')
        self.bind("<Button-1>",self.OnClick)
    def __changebgColor(self, color):
        for elem in self.bgElements:
            self.itemconfig(elem, fill=color, outline=color)        
    def __changetextColor(self, color):
        for elem in self.textElements:
            self.itemconfig(elem, fill=color)        
    def disable(self):
        self.state = 0
        self.__changebgColor(self.bgElementsColor[0])
        self.__changetextColor(self.textElementsColor[0])
    def enable(self):
        self.state = 1
        if self.__active:
            index = 2
        else:
            index = 1
        for elem in self.bgElements:
            self.itemconfig(elem, fill=self.bgElementsColor[index], outline=self.bgElementsColor[index])
        for elem in self.textElements:
            self.itemconfig(elem, fill=self.textElementsColor[index])
    def OnClick(self, event):
        if self.state>0:
            if self.exFunctionParams:
                self.exFunction(self.exFunctionParams)
            else:
                self.exFunction()
        if self.state==1:
            if self.__schalter:
                Thread(target=self.animationOn, args=()).start()
                self.state = 2
            else:
                Thread(target=self.animationOnOff, args=()).start()
        else:
            Thread(target=self.animationOff, args=()).start()
            self.state = 1
    def clicked(self):
        if self.state==2:
            return 1
        return 0
    def animationOn(self):
        with self.__lock:
            bgcolor = self.bgElementsColor[2]
            textcolor = self.textElementsColor[2]
            if bgcolor.luminance<=0.5:
                bgvalue = bgcolor.luminance/2
            else:
                bgvalue = (1-bgcolor.luminance)/2
            bgcolor.luminance -= bgvalue
            self.__changebgColor(bgcolor.hex)
            if textcolor.luminance<=0.5:
                textvalue = textcolor.luminance/2
            else:
                textvalue = (1-textcolor.luminance)/2
            textcolor.luminance -= textvalue
            self.__changetextColor(textcolor.hex)
            for x in range(15):
                bgcolor.luminance = bgcolor.luminance +bgvalue/15
                textcolor.luminance = textcolor.luminance +textvalue/15
                self.__changetextColor(textcolor.hex)
                self.__changebgColor(bgcolor.hex)                
                time.sleep(0.01)            
    def animationOff(self):
        with self.__lock:
            bgcolor = self.bgElementsColor[2]
            textcolor = self.textElementsColor[2]
            if bgcolor.luminance<=0.5:
                bgvalue = bgcolor.luminance/2
            else:
                bgvalue = (1-bgcolor.luminance)/2
            self.__changebgColor(bgcolor.hex)
            if textcolor.luminance<=0.5:
                textvalue = textcolor.luminance/2
            else:
                textvalue = (1-textcolor.luminance)/2
            self.__changetextColor(textcolor.hex)
            for x in range(15):
                bgcolor.luminance = bgcolor.luminance -bgvalue/15
                textcolor.luminance = textcolor.luminance -textvalue/15
                self.__changetextColor(textcolor.hex)
                self.__changebgColor(bgcolor.hex)                
                time.sleep(0.01)
            bgcolor.luminance = bgcolor.luminance +bgvalue
            textcolor.luminance = textcolor.luminance +textvalue        
            self.__changetextColor(self.textElementsColor[1])
            self.__changebgColor(self.bgElementsColor[1]) 
    def animationOnOff(self):
        self.animationOn()
        self.animationOff()
        
        
class StandardButton(Button):
    def __init__(self, root, text, width=120, height=50, background="black", font=["LCARSGTJ3", "16"], exFunction=None, exFunctionParams=None, color="#99ccff"):
        Button.__init__(self, root, width=width, height=height, background=background, font=font)
        self.exFunction = exFunction
        self.exFunctionParams = exFunctionParams
        self.text = text
        self.bgElementsColor[1] = Color(color)
        self.build()
    def build(self):
        coords = [0,0,self.width, self.height]
        self.bgElements.append(self.create_rectangle(coords, fill=self.bgElementsColor[1], outline=self.bgElementsColor[1]))
        coords = [self.width-5, self.height]
        self.textElements.append(self.create_text(coords, fill=self.textElementsColor[1], text=self.text, font=self.font, anchor="se"))