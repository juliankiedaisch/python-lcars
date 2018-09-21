import requests, datetime
from requests.auth import HTTPBasicAuth
import xml.etree.ElementTree as ET
from threading import Thread

class timeZone:
    def __init__(self, data):
        self.id = None
        self.location = None
        self.standard = None
        self.daylight = None
        self.__make_timezone(data)
    def __make_timezone(self, data):
        standard = None
        for line in data.split("\n"):
            item = line.split(":")
            if item:
                if item[0]=="ZID":
                    self.id = item[1]
                if item[0]=="X-LIC-LOCATION":
                    self.location = item[1]
        #Standard
        temp=0
        while temp>=0:
            temp = data.find("BEGIN:STANDARD\n", temp)
            if temp>0:
                end = data.find("END:STANDARD\n", temp)
                if end>-1:
                    tzname, ofrom, oto = self.__make_timezone2(data[temp+15:end])
                    if ofrom and oto and tzname:
                        self.standard = {"tzname": tzname, "tzoffsetfrom": ofrom, "tzoffsetto": oto}
                temp +=1
        #Daylight
        temp=0
        while temp>=0:
            temp = data.find("BEGIN:DAYLIGHT\n", temp)
            if temp>0:
                end = data.find("END:DAYLIGHT\n", temp)
                if end>-1:
                    tzname, ofrom, oto = self.__make_timezone2(data[temp+16:end])
                    if ofrom and oto and tzname:
                        self.daylight = {"tzname": tzname, "tzoffsetfrom": ofrom, "tzoffsetto": oto}
                temp +=1
    def __make_timezone2(self,data):
        offsetfrom = None
        offsetto = None
        tzname = None
        for line in data.split("\n"):
            item = line.split(":")
            if item:
                if item[0]=="TZOFFSETFROM":
                    offsetfrom = item[1]
                elif item[0]=="TZOFFSETTO":
                    offsetto = item[1]
                elif item[0]=="TZNAME":
                    tzname = item[1]
        return tzname, offsetfrom, offsetto

class VEVENT:
    def __init__(self, data, timezones):
        self.start = None
        self.end = None
        self.uid = None
        self.last_modfied = None
        self.location = None
        self.summary = None
        self.rrule = None
        self.allday = False
        self.created = None
        self.timezone = None
        self.__timezones = timezones
        self.__worker(data)
    def __worker(self, data):
        #Alarm rausschneiden:
        while True:
            a = data.find("BEGIN:VALARM\n")
            b = data.find("END:VALARM\n")
            if a<b:
                data = data[:a] + data[b+11:]
            else:
                #print temp
                break
        #print data
        for line in data.split("\n"):
            item = line.split(":", 1)
            if item:
                if item[0][:7]=="DTSTART":
                    t = item[0].split(";")
                    try:
                        if t[1] == "VALUE=DATE":
                            self.start=datetime.datetime(int(item[1][:4]), int(item[1][4:6]), int(item[1][6:8]))
                            self.allday = True
                        else:
                            s = t[1].split("=")
                            self.start= datetime.datetime.strptime(item[1][:15], "%Y%m%dT%H%M%S" )
                            temp = filter(lambda x: x.id == s[1], self.__timezones)
                            if temp:
                                self.timezone = temp[0]
                    except IndexError:
                        self.start= datetime.datetime.strptime(item[1][:15], "%Y%m%dT%H%M%S" )                       
                elif item[0][:5]=="DTEND":
                    t = item[0].split(";")
                    try:
                        if t[1] == "VALUE=DATE":
                            self.end=datetime.datetime(int(item[1][:4]), int(item[1][4:6]), int(item[1][6:8]))
                        else:
                            self.end= datetime.datetime.strptime(item[1][:15], "%Y%m%dT%H%M%S" )
                    except IndexError:
                         self.end= datetime.datetime.strptime(item[1][:15], "%Y%m%dT%H%M%S" )
                elif item[0]=="UID":
                    self.uid = item[1]
                elif item[0]=="CREATED":
                    self.created = datetime.datetime.strptime(item[1][:15], "%Y%m%dT%H%M%S" )
                elif item[0]=="LAST-MODIFIED":
                    self.last_modified = datetime.datetime.strptime(item[1][:15], "%Y%m%dT%H%M%S" )
                elif item[0]=="SUMMARY":
                    self.summary = item[1]
                elif item[0]=="LOCATION":
                    self.location = item[1]
                elif item[0]=="RRULE":
                    self.rrule = item[1].split(";")
        if not self.end:
            self.end = self.start + datetime.timedelta(days=1)
class Event:
    def __init__(self, href, data, calendar):
        self.href = href
        self.vevent = None
        self.calendar = calendar
        self.timezones = []
        self.__worker(data)
    def __worker(self, data):
        #VTIMEZONES:
        temp=0
        while temp>=0:
            temp = data.find("BEGIN:VTIMEZONE\n", temp)
            if temp>0:
                end = data.find("END:VTIMEZONE\n", temp)
                if end>-1:
                    self.timezones.append(timeZone(data[temp+17:end]))
                temp +=1
        #vevent
            start = data.find("BEGIN:VEVENT\n")
            end = data.find("END:VEVENT\n")
            if start<end:
                self.vevent = VEVENT(data[start+13:end], self.timezones)

class Kalender:
    def __init__(self, href, name, ctag):
        self.href = href
        self.name = name
        self.ctag = ctag
class DavClient:
    def __init__(self, url="https://cloud.jkiedaisch.de", user="julian", password="Alpha1,1"):
        self.url = url
        self.user = user
        self.password = password
        self.auth = HTTPBasicAuth(self.user,self.password)
        self.calendars = self.__getCalendars()
        self.__eventlist = []
    def __worker(self, calendar, start, end):
        self.__eventlist += self.getEventsByDate(calendar, start, end)
    def getWeek(self, datum):


        start = datetime.datetime.today() + datetime.timedelta(weeks=6)
        end= start + datetime.timedelta(weeks=1)

        worker = [Thread(target=doit, args=(elem, start, end, events,)) for elem in dav.calendars]
        for w in worker:
            w.start()
        for w in worker:
            w.join()
        for item in events:
            print item.vevent.summary, item.vevent.start.day, item.vevent.end.day
    def __getCalendars(self):
        headers = {'Depth': "1", "Content-Type" : "application/xml; charset=\"utf-8\""}
        xml="""<d:propfind xmlns:d="DAV:" xmlns:cs="http://calendarserver.org/ns/">
          <d:prop>
             <d:displayname />
             <cs:getctag />
          </d:prop>
        </d:propfind>"""
        url = self.url + "/remote.php/dav/calendars/" + self.user + "/"
        r = requests.request("PROPFIND", url , data=xml, headers=headers, auth=self.auth, verify=True)
        root = ET.fromstring(r.content)
        kalenderliste = []
        for elem in root:
            ctag = ""
            displayname = ""
            status = ""
            href = ""
            for elem2 in elem:
                if elem2.tag =="{DAV:}href":
                    href = elem2.text
                elif elem2.tag =="{DAV:}propstat":
                    for elem3 in elem2:
                        if elem3.tag =="{DAV:}status":
                            status = elem3.text
                        elif elem3.tag =="{DAV:}prop":
                            for elem4 in elem3:
                                if elem4.tag =="{DAV:}displayname":
                                    displayname = elem4.text
                                elif elem4.tag =="{http://calendarserver.org/ns/}getctag":
                                    ctag = elem4.text
                                else:
                                    pass
            if status == "HTTP/1.1 200 OK":
                kalenderliste.append(Kalender(href, displayname, ctag))
        return kalenderliste

    def getEventsByDate(self, calendar, start, end=None):
        temp = []
        headers = {'Depth': "1", "Content-Type" : "application/xml; charset=\"utf-8\""}
        xstart = start.strftime("%Y%m%dT%H%M%SZ")
        if end and start<end:
            xend = end.strftime("%Y%m%dT%H%M%SZ")
        else:
            xend = (start + datetime.timedelta(days=1)).strftime("%Y%m%dT%H%M%SZ")

        xml="""<c:calendar-query xmlns:d="DAV:" xmlns:c="urn:ietf:params:xml:ns:caldav">
                    <d:prop>
                        <c:calendar-data />
                    </d:prop>
                    <c:filter>
                        <c:comp-filter name="VCALENDAR">
                            <c:comp-filter name="VEVENT">
                                <c:time-range  start="%s" end="%s"/>
                            </c:comp-filter>
                        </c:comp-filter>
                    </c:filter>
                </c:calendar-query>""" % (xstart, xend)
        url = self.url + calendar.href
        r = requests.request("REPORT", url , data=xml, headers=headers, auth=self.auth, verify=True)
        root = ET.fromstring(r.content)
        for elem in root:
            href = ""
            data = None
            if elem.tag =="{DAV:}response":
                for elem2 in elem:
                    if elem2.tag =="{DAV:}href":
                        href = elem2.text
                    elif elem2.tag =="{DAV:}propstat":
                        for elem3 in elem2:
                            if elem3.tag =="{DAV:}prop":
                                for elem4 in elem3:
                                    if elem4.tag =="{urn:ietf:params:xml:ns:caldav}calendar-data":
                                        data = elem4.text
            if data:
                temp.append(Event(href, data, calendar))
        return temp
    def checkForCalendarChange(self):
        result = []
        for elem in self.__getCalendars():
            temp = filter(lambda x: x.href == elem.href, self.calendars)
            if temp:
                if temp[0].href == elem.href and temp[0].ctag != elem.ctag:
                    result.append(elem)
                    self.calendars.remove(temp[0])
                    self.calendars.append(elem)
                continue
            else:
                result.append(elem)
                self.calendars.append(elem)
        return result


