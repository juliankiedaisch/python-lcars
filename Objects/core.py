from threading import Thread, Condition
from Module.Kalender.code import DavClient
import logging
import time, datetime
logger = logging.getLogger(__name__)

logging.basicConfig(level=logging.DEBUG,
                    format='[%(asctime)s %(threadName)s] %(message)s',
                    datefmt='%H:%M:%S')


class Core:
    def __init__(self):
        self.modulList = []
    def addModule(self, Modul):
        if filter(lambda x: x.index == Modul.index, self.modulList):
            return 0
        self.modulList.append(Modul)
        return 1
    def removeModule(self, Modul):
        self.modulList.remove(Modul)
    def removeModuleByIndex(self, index):
        for elem in self.modulList:
            if elem.index == index:
                self.modulList.remove(elem)
    def getModuleByIndex(self, index):
        return filter(lambda x: x.index == index, self.modulList)
    def getModuleByState(self, state):
        return filter(lambda x: x.state == state, self.modulList)
    def shutdown(self):
        for elem in self.modulList:
            elem.stop()
        for elem in self.modulList:
            elem.join()



class Modul(Thread):
    def __init__(self, index):
        self.__state = Condition()
        self.__index = index
        self.__status = True
        self.__paused = True
        Thread.__init__(self)
        self.start()
    @property
    def index(self):
        return self.__index
    def run(self):
        self.resume()
        while self.__status:
            with self.__state:
                if self.__paused:
                    self.__state.wait()
            self.threadFunction()
    def threadFunction(self):
        time.sleep(1)
    def resume(self):
        with self.__state:
            self.__paused = False
            self.__state.notify()
    def pause(self):
        with self.__state:
            self.__paused = True
    @property
    def state(self):
        if self.__status:
            if (self.__paused):
                return 2
            else:
                return 1
        else:
            return 0
    def stop(self):
        self.__status = False
    
    
class Kalender(Modul):
    def __init__(self):
        self.__dav = DavClient()
        self.__eventList = []
        self.__new = 1
        self.__start = datetime.datetime.today() - datetime.timedelta(weeks=52)
        self.__end = datetime.datetime.today() + datetime.timedelta(weeks=52)
        Modul.__init__(self, "calendar")
    def __getEvents(self, calendar, start, end, list):
        list += self.__dav.getEventsByDate(calendar, start, end)        
    def threadFunction(self):
        if self.__new:
            worker = [Thread(target=self.__getEvents, args=(elem, self.__start, self.__end, self.__eventList,)) for elem in self.__dav.calendars]
            for w in worker:
                w.start()
            for w in worker:
                w.join()
            self.__new = 0
        else:
            temp = self.__dav.checkForCalendarChange()
            for elem in temp:
                liste = filter(lambda x: x.calendar.href == elem.href, self.__eventList)
                for event in liste:
                    self.__eventList.remove(event)
                self.__getEvents(elem, self.__start, self.__end, self.__eventList)
        time.sleep(60)
    def getWeek(self, date):
        temp = filter(lambda x: x.vevent.start>=date, self.__eventList)
        return filter(lambda x: x.vevent.start<=date+datetime.timedelta(weeks=1), temp)


