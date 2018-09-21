# -*- coding: iso-8859-1 -*-
from Tkinter import *
from gui import MainGui
from Objects.core import Core

root = Tk()
root.geometry("1200x800")
MainCore = Core()
#Hauptseite
Gui = MainGui(root, MainCore)

root.mainloop()