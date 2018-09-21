from threading import Thread, Lock

class Element:
    def __init__(self, root):
        self.root = root
        self.elementList = []
    def remove(self):
        for elem in self.elementList:
            self.root.delete(elem)


class coordinaten:
    def __init__(self, coords):
        self.__coords=coords
    @property
    def x1(self):
        return self.__coords[0]
    @property
    def x2(self):
        return self.__coords[2]
    @property
    def y1(self):
        return self.__coords[1]
    @property
    def y2(self):
        return self.__coords[3]
    @property
    def width(self):
        return abs(self.__coords[0]-self.__coords[2])
    @property
    def height(self):
        return abs(self.__coords[1]-self.__coords[3])

class LeisteEinfach(Element):
    def __init__(self, root, coords, fill="#9999ff", pieces=1):
        Element.__init__(self, root)
        self.__coords = coordinaten(coords)
        self.__fill= fill
        self.__pieces = pieces
        self.build()
    def build(self):
        coords = [self.__coords.x1,self.__coords.y1, self.__coords.x1+self.__coords.height, self.__coords.y2]
        self.elementList.append(self.root.create_arc(coords, start=90, extent=180, fill=self.__fill, outline=self.__fill))
        coords = [self.__coords.x1+self.__coords.height/2,self.__coords.y1, self.__coords.x1+self.__coords.height, self.__coords.y2]
        self.elementList.append(self.root.create_rectangle(coords, fill=self.__fill, outline=self.__fill))
        
        coords = [self.__coords.x2,self.__coords.y1, self.__coords.x2-self.__coords.height, self.__coords.y2]
        self.elementList.append(self.root.create_arc(coords, start=-90, extent=180, fill=self.__fill, outline=self.__fill))
        coords = [self.__coords.x2-self.__coords.height/2,self.__coords.y1, self.__coords.x2-self.__coords.height, self.__coords.y2]
        self.elementList.append(self.root.create_rectangle(coords, fill=self.__fill, outline=self.__fill))
        
        pieceLength = (self.__coords.width-2*self.__coords.height-10*(self.__pieces+1))/self.__pieces
        for x in range(self.__pieces):
            coords = [self.__coords.x1+self.__coords.height+10+x*(10+pieceLength),self.__coords.y1, self.__coords.x1+self.__coords.height+(x+1)*(10+pieceLength), self.__coords.y2]
            self.elementList.append(self.root.create_rectangle(coords, fill=self.__fill, outline=self.__fill))        

class AbschlussObenRechts(Element):
    def __init__(self, root, coords,fill="#9999ff",r1=60,r2=20, background="black"):
        Element.__init__(self, root)
        self.__coords = coordinaten(coords)
        self.__radius = [r1,r2]
        self.__fill= fill
        self.__background = background
        self.build()
    def build(self):
        #x,y in der oberen rechten Ecke
        radius1 = self.__radius[0]
        radius2 = self.__radius[1]
        dy = self.__coords.y2
        dx = self.__coords.x2
        x = self.__coords.x1
        y = self.__coords.y1
        
        if dy+radius2>radius1:
            coords=x+radius2,y+radius1,x+radius2+dx,y+dy+radius2
            self.elementList.append(self.root.create_rectangle(coords, fill=self.__fill, outline=self.__fill))

        #Rectangle
        coords=x-dx,y+dy+radius2,x-radius1, y+radius1
        self.elementList.append(self.root.create_rectangle(coords, fill=self.__fill, outline=self.__fill))
        coords=x-dx-radius2,y,x-radius1,y+radius2+dy
        self.elementList.append(self.root.create_rectangle(coords, fill=self.__fill, outline=self.__fill))
        #Arcs
        coords=x-2*radius1,y,x,y+2*radius1
        self.elementList.append(self.root.create_arc(coords, start=0, extent=90, fill=self.__fill, outline=self.__fill))

        coords=x-2*radius2-dx,y+dy,x-dx-1,y+dy+2*radius2
        self.elementList.append(self.root.create_arc(coords, start=0, extent=90, fill=self.__background, outline=self.__background))

class AbschlussUntenRechts(Element):
    def __init__(self, root, coords,fill="#9999ff",r1=60,r2=20, background="black"):
        Element.__init__(self, root)
        self.__coords = coordinaten(coords)
        self.__radius = [r1,r2]
        self.__fill= fill
        self.__background = background
        self.build()
    def build(self):
        #x,y in der unteren linken Ecke
        radius1 = self.__radius[0]
        radius2 = self.__radius[1]
        dy = self.__coords.y2
        dx = self.__coords.x2
        x = self.__coords.x1
        y = self.__coords.y1
        
        if dy+radius2>radius1:
            coords=x-dx,y-radius1,x,y-dy-radius2
            self.elementList.append(self.root.create_rectangle(coords, fill=self.__fill, outline=self.__fill))
        #Rectangle
        coords=x-(radius2+dx),y,x+1-dx, y-radius2-dy+1
        self.elementList.append(self.root.create_rectangle(coords, fill=self.__fill, outline=self.__fill))
        coords=x-dx,y,x-radius1,y-radius1
        self.elementList.append(self.root.create_rectangle(coords, fill=self.__fill, outline=self.__fill))
        #Arcs
        coords=x-2*radius1,y-2*radius1,x,y
        self.elementList.append(self.root.create_arc(coords, start=270, extent=90, fill=self.__fill, outline=self.__fill))

        coords=x-2*radius2-dx,y-dy,x-1-dx,y-dy-2*radius2
        self.elementList.append(self.root.create_arc(coords, start=270, extent=90, fill=self.__background, outline=self.__background))

class AbschlussObenLinks(Element):
    def __init__(self, root, coords,fill="#9999ff",r1=60,r2=20, background="black"):
        Element.__init__(self, root)
        self.__coords = coordinaten(coords)
        self.__radius = [r1,r2]
        self.__fill= fill
        self.__background = background
        self.build()
    def build(self):
        #x,y in der oberen rechten Ecke
        radius1 = self.__radius[0]
        radius2 = self.__radius[1]
        dy = self.__coords.y2
        dx = self.__coords.x2
        x = self.__coords.x1
        y = self.__coords.y1
        
        if dy+radius2>radius1:
            coords=x,y+radius1,x+dx,y+dy+radius2
            self.elementList.append(self.root.create_rectangle(coords, fill=self.__fill, outline=self.__fill))


        #Rectangle
        coords=x+dx+1,y,x+dx+radius2, y+radius2+dy-1
        self.elementList.append(self.root.create_rectangle(coords, fill=self.__fill, outline=self.__fill))
        coords=x+radius1,y,x+dx,y+radius1
        self.elementList.append(self.root.create_rectangle(coords, fill=self.__fill, outline=self.__fill))
        #Arcs
        coords=x,y,x+2*radius1,y+2*radius1
        self.elementList.append(self.root.create_arc(coords, start=90, extent=90, fill=self.__fill, outline=self.__fill))

        coords=x+dx+1,y+dy+1,x+dx+2*radius2,y+dy+2*radius2
        self.elementList.append(self.root.create_arc(coords, start=90, extent=90, fill=self.__background, outline=self.__background))

class AbschlussUntenLinks(Element):
    def __init__(self, root, coords,fill="#9999ff",r1=60,r2=20, background="black"):
        Element.__init__(self, root)
        self.__coords = coordinaten(coords)
        self.__radius = [r1,r2]
        self.__fill= fill
        self.__background = background
        self.build()
    def build(self):
        #x,y in der unteren rechten Ecke
        radius1 = self.__radius[0]
        radius2 = self.__radius[1]
        dy = self.__coords.y2
        dx = self.__coords.x2
        x = self.__coords.x1
        y = self.__coords.y1        
        
        if dy+radius2>radius1:
            coords=x,y-radius1,x+dx,y-dy-radius2
            self.elementList.append(self.root.create_rectangle(coords, fill=self.__fill, outline=self.__fill))
        #Rectangle
        coords=x+dx+1,y,x+dx+radius2, y-radius2-dy
        self.elementList.append(self.root.create_rectangle(coords, fill=self.__fill, outline=self.__fill))
        coords=x+radius1,y,x+dx,y-radius1
        self.elementList.append(self.root.create_rectangle(coords, fill=self.__fill, outline=self.__fill))
        #Arcs
        coords=x,y,x+2*radius1,y-2*radius1
        self.elementList.append(self.root.create_arc(coords, start=180, extent=90, fill=self.__fill, outline=self.__fill))

        coords=x+dx+1,y-dy,x+dx+2*radius2,y-dy-2*radius2
        self.elementList.append(self.root.create_arc(coords, start=180, extent=90, fill=self.__background, outline=self.__background))

class AbschlussLinks(Element):
    def __init__(self, root, coords, fill="#9999ff"):
        Element.__init__(self, root)
        self.__coords = coordinaten(coords)
        self.__fill= fill
        self.build()
    def build(self):
        coords = [self.__coords.x1,self.__coords.y1, self.__coords.x1+self.__coords.height, self.__coords.y2]
        self.elementList.append(self.root.create_arc(coords, start=90, extent=180, fill=self.__fill, outline=self.__fill))
        coords = [self.__coords.x1+self.__coords.height/2,self.__coords.y1, self.__coords.x2, self.__coords.y2]
        self.elementList.append(self.root.create_rectangle(coords, fill=self.__fill, outline=self.__fill))
        
class AbschlussRechts(Element):
    def __init__(self, root, coords, fill="#9999ff"):
        Element.__init__(self, root)
        self.__coords = coordinaten(coords)
        self.__fill= fill
        self.build()
    def build(self):
        coords = [self.__coords.x2,self.__coords.y1, self.__coords.x2-self.__coords.height, self.__coords.y2]
        self.elementList.append(self.root.create_arc(coords, start=-90, extent=180, fill=self.__fill, outline=self.__fill))
        coords = [self.__coords.x2-self.__coords.height/2,self.__coords.y1, self.__coords.x1, self.__coords.y2]
        self.elementList.append(self.root.create_rectangle(coords, fill=self.__fill, outline=self.__fill))
        
class AbschlussUnten(Element):
    def __init__(self, root, coords, fill="#9999ff", radius=10):
        Element.__init__(self, root)
        self.__coords = coordinaten(coords)
        self.__fill= fill
        self.__radius = radius
        self.build()
    def build(self):
        coords = [self.__coords.x1,self.__coords.y2-2*self.__radius, self.__coords.x1+2*self.__radius, self.__coords.y2]
        self.elementList.append(self.root.create_arc(coords, start=180, extent=90, fill=self.__fill, outline=self.__fill))
        coords = [self.__coords.x2-2*self.__radius,self.__coords.y2-2*self.__radius, self.__coords.x2, self.__coords.y2]
        self.elementList.append(self.root.create_arc(coords, start=270, extent=90, fill=self.__fill, outline=self.__fill))
        coords = [self.__coords.x1,self.__coords.y1, self.__coords.x2, self.__coords.y2-self.__radius]
        self.elementList.append(self.root.create_rectangle(coords, fill=self.__fill, outline=self.__fill))
        coords = [self.__coords.x1+self.__radius,self.__coords.y2-self.__radius, self.__coords.x2-self.__radius, self.__coords.y2]
        self.elementList.append(self.root.create_rectangle(coords, fill=self.__fill, outline=self.__fill))
        
class LaeuferLinks(AbschlussLinks):
    def __init__(self, root, coords, fill="#9999ff"):
       AbschlussLinks.__init__(self, root, coords, fill=fill)
       self.coords = coordinaten(coords)
    def move(self, x, y):
        for elem in self.elementList:
            self.root.move(elem, x, y)
            
class LaeuferRechts(Element):
    def __init__(self, root, coords, fill="#9999ff", background="black", radius=10):
        Element.__init__(self, root)
        self.__radius = radius
        self.__coords = coordinaten(coords)
        self.__background = background
        self.__fill = fill
        self.__build()
    def __build(self):
        coords = [self.__coords.x1,self.__coords.y1, self.__coords.x2, self.__coords.y2]
        self.elementList.append(self.root.create_rectangle(coords, fill=self.__fill, outline=self.__fill))

        coords = [self.__coords.x1,self.__coords.y1, self.__coords.x2-self.__radius, self.__coords.y1+self.__radius]
        self.elementList.append(self.root.create_rectangle(coords, fill=self.__background, outline=self.__background))
        coords = [self.__coords.x1,self.__coords.y2, self.__coords.x2-self.__radius, self.__coords.y2-self.__radius]
        self.elementList.append(self.root.create_rectangle(coords, fill=self.__background, outline=self.__background))
         
        coords = [self.__coords.x2-2*self.__radius,self.__coords.y1-self.__radius, self.__coords.x2+1,self.__coords.y1+self.__radius]
        self.elementList.append(self.root.create_arc(coords, start=270, extent=90, fill=self.__background, outline=self.__background))        
        coords = [self.__coords.x2-2*self.__radius,self.__coords.y2-self.__radius, self.__coords.x2+1,self.__coords.y2+self.__radius]
        self.elementList.append(self.root.create_arc(coords, start=90, extent=-90, fill=self.__background, outline=self.__background))        
       
    def move(self, x, y):
        for elem in self.elementList:
            self.root.move(elem, x, y)