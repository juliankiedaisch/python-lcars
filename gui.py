# -*- coding: iso-8859-1 -*-
from Tkinter import *
import tkFont, time
from colour import Color
from threading import Thread, Lock
from Objects.button import StandardButton
from Objects.elements import *
from Objects.core import Modul

class destroyButton(StandardButton):
    def OnClick(self, event):
        if self.state>0:
            if self.exFunctionParams:
                self.exFunction(self.exFunctionParams)
            else:
                self.exFunction() 

class Zeit(Modul):
    def __init__(self, canvas,text):
        self.__text = text
        self.__canvas = canvas
        Modul.__init__(self, "Zeit")
    def threadFunction(self):
        self.__canvas.itemconfig(self.__text, text=time.strftime("%H:%M:%S"))
        time.sleep(1)

class MainGui:
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

    def laufer(self, y):
        with self.__lock:
            if self.__position<y:
                while self.__position<y:
                    self.__position+=1
                    for elem in self.__lauferObj:
                        elem.move(0,1)   
            else:
                while self.__position>y:
                    self.__position-=1
                    for elem in self.__lauferObj:
                        elem.move(0,-1)
    def beenden(self):
        self.core.shutdown()
        self.__root.destroy()
    def __build(self):
        #Von Rechts Oben nach Links unten
        AbschlussRechts(self.__canvas, [self.__width-45,0, self.__width, 40], fill=self.__objfarbe)
        self.__canvas.create_rectangle([self.__width-50,0,self.__width-60,40], fill=self.__objfarbe, outline=self.__objfarbe)        
        self.__canvas.create_text(self.__width-70,52, text="Familienterminal", fill=self.__headcolor, font=self.__headfont, anchor="se")
        self.__canvas.create_rectangle([803,0,self.__width-320,40], fill=self.__objfarbe, outline=self.__objfarbe)
        self.__canvas.create_rectangle([415,0,695,40], fill=self.__objfarbe, outline=self.__objfarbe)
        self.__zeitObj = self.__canvas.create_text(302,52, text="00:00:00", fill=self.__headcolor, font=self.__headfont, anchor="sw")
        self.__canvas.create_rectangle([200,0,280,40], fill=self.__objfarbe, outline=self.__objfarbe)
        self.__canvas.create_rectangle([285,0,295,40], fill=self.__objfarbe, outline=self.__objfarbe)
        AbschlussObenLinks(self.__canvas, [40,0,140,40], fill=self.__objfarbe)
        self.__canvas.create_rectangle([40,60,180,100], fill=self.__objfarbe, outline=self.__objfarbe)


        self.__canvas.create_rectangle([40,self.__height-85,180,self.__height-95], fill=self.__objfarbe, outline=self.__objfarbe)
        AbschlussUnten(self.__canvas, [40,self.__height-80,180,self.__height], fill=self.__objfarbe) 
        #Zeit
        self.__zeit = Zeit(self.__canvas, self.__zeitObj)
        self.core.addModule(self.__zeit)
        #Laeufer
        self.__lauferObj.append(LaeuferLinks(self.__canvas, [0,105,35,154], fill=self.__objfarbe2))
        self.__lauferObj.append(LaeuferRechts(self.__canvas, [185,75,220,184], fill=self.__objfarbe2, radius=30))
        #Mitte Leiste
        self.__canvas.create_rectangle([220,80,235,self.__height-90], fill=self.__objfarbe2, outline=self.__objfarbe2)
        AbschlussUnten(self.__canvas, [220,self.__height-80,235,self.__height], fill=self.__objfarbe2, radius=5)
        AbschlussObenLinks(self.__canvas, [220,60,15,40], fill=self.__objfarbe2, r1=20, r2=10)
        self.__canvas.create_rectangle([245,60,295,100], fill=self.__objfarbe2, outline=self.__objfarbe2)

        #Buttons
        b0 = destroyButton(self.__canvas, "Beenden", width=100, height=40, exFunction=self.beenden, color="#cc0000")
        self.__canvas.create_window(700,1, window=b0, anchor="nw")
        b1 = StandardButton(self.__canvas, "Start", width=140, exFunction=self.clickAction, exFunctionParams=105)
        self.__canvas.create_window(40,105, window=b1, anchor="nw")
        b2 = StandardButton(self.__canvas, "Umweltkontrollen", width=140, exFunction=self.clickAction, color=self.__objfarbe, exFunctionParams=160)
        self.__canvas.create_window(40,160, window=b2, anchor="nw")
        b3 = StandardButton(self.__canvas, "Kalender", width=140, exFunction=self.clickAction, color="#009999", exFunctionParams=215)
        self.__canvas.create_window(40,215, window=b3, anchor="nw")
        b4 = StandardButton(self.__canvas, "Nahverkehr", width=140, exFunction=self.clickAction, color="#003366", exFunctionParams=270)
        self.__canvas.create_window(40,270, window=b4, anchor="nw")
        b5 = StandardButton(self.__canvas, "Medien", width=140, exFunction=self.clickAction, color="#ccddbb", exFunctionParams=325)
        self.__canvas.create_window(40,325, window=b5, anchor="nw")
    def clickAction(self,params):
        #self.laufer(params)
        Thread(target=self.laufer, args=([params])).start()