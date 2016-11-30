import urllib.request
import xmltodict
import sqlite3

def DbRead():
    db = sqlite3.connect("C:/Users/ilana/yuData.db")
    #curse = db.cursor();

    dbFile = db.execute("SELECT * FROM events");
    results = dbFile.fetchall();

    print(results);
    print("DB read complete");
    db.close();

def DbWrite(ID, Title, Description, Location, Date, Time, Duration, Featured):
    db = sqlite3.connect("C:/Users/ilana/yuData.db")
    featuredInt = 0

    if Featured:
        featuredInt = 1

    Description = "Description"

    sql = 'INSERT INTO events VALUES(' + str(ID) + ',"' + Title + '","' + Description + '","' + Location + '","' + Date + '","' + Time + '","' + Duration + '",' + str(featuredInt) + ")";
    print(sql)

    db.execute(sql);
    db.commit()

    print("DB write complete");
    db.close();

def parse(desc):
    newDesc = desc.split("<br/>")
    return newDesc

def getDate(info):
    date = info[1]
    print(date)
    return date

def getTime(datex):
    splitt = datex.split(" ")
    if len(splitt)>=4 and "&nbsp;&ndash;&nbsp;" in splitt[4]:
        fullTime = splitt[4]
        time = fullTime.split("&nbsp;&ndash;&nbsp;")
        startTime = time[0]
        endTime = time[1]
    else:
        a = False
        for s in splitt:
            if "&nbsp;&ndash;" in s:
                startTime = s.split("&nbsp;&ndash;")[0]
                a = True
        if a:
            endTime = splitt[8]
        else:
            startTime = "00:00AM"
            endTime = "11:59PM"
    diff = getDif(startTime, endTime)
    startTime = fixTime(startTime, endTime)
    print(endTime)
    print(diff)

def fixTime(time, end):
    t = time.upper()
    e = end.upper()

    if ":" not in t:
        if "AM" in t:
            t = t.split("AM")[0].replace(" ","")+":00AM"
        elif "PM" in t:
            t = t.split("PM")[0].replace(" ","")+":00PM"
        else:
            t = t+":00"
    if ":" not in e:
        if "AM" in e:
            e = e.split("AM")[0].replace(" ","")+":00AM"
        elif "PM" in e:
            e = e.split("PM")[0].replace(" ","")+":00PM"
        else:
            e = e+":00"
    if ":" in t:
        if "AM" in t:
            if len(t.split("AM")[0])==5:
                t = t
            else:
                t = "0" + t
            t = t.split("AM")[0]
        elif "PM" in t:
            a = int(t.split(":")[0]) + 12
            t = "" + str(a) + ":" + t.split(":")[1]
            t = t.split("PM")[0]
        elif "PM" in e:
            if int(t.split(":")[0])<int(e.split(":")[0]):
                a = int(t.split(":")[0]) + 12
                t = "" + str(a) + ":" + t.split(":")[1]
            else:
                if len(t) == 5:
                    t = t
                else:
                    t = "0" + t
        elif "AM" in e:
            if int(t.split(":")[0])<int(e.split(":")[0]):
                if len(t) == 5:
                    t = t
                else:
                    t = "0" + t
            else:
                a = int(t.split(":")[0]) + 12
                t = "" + a + ":" + t.split(":")[1]
    print(t)
    return t


def getDif(a, b):
    start = a.upper()
    end = b.upper()
    hours = 0
    mins = 0

    if "AM" in start:
        start = start.split("AM", 1)[0].replace(" ","")

    if "PM" in start:
        start = start.split("PM", 1)[0].replace(" ","")

    if "AM" in end:
        end = end.split("AM", 1)[0].replace(" ","")

    if "PM" in end:
        end = end.split("PM", 1)[0].replace(" ","")

    if ":" not in start:
        start = start + ":00"
    if ":" not in end:
        end = end + ":00"

    c = int(start.split(":")[0])
    d = int(end.split(":")[0])
    min1 = int(start.split(":")[1])
    min2 = int(end.split(":")[1])
    if c < d:
        if "AM" in a.upper() and "PM" in b.upper():
            hours = d + 12 - c
        else:
            hours = d - c
    else:
        hours = d + 12 - c

    if min1>min2:
        if min2==0:
            mins = 60-min1
        else:
            mins = min1-min2
        hours = hours-1
    else:
        mins = min2-min1

    mins = str(mins)
    if len(mins)==1:
        mins = "0" + mins

    #print("Diff: " + str(hours) + ":" + str(mins))
    print("Duration: " + str(hours + int(mins)/60))
    return str(hours + int(mins)/60)

def getTitle(obj):
    return obj['title']

def getDate(obj):
    return obj['category']

def getLoc(obj):
    return parse(obj['description'])[0]

def getDescription(obj):
    return obj['description']

def getDuration(obj):
    d = parse(obj['description'])

    datex = d[1]
    splitt = datex.split(" ")
    if len(splitt) >= 4 and "&nbsp;&ndash;&nbsp;" in splitt[4]:
        fullTime = splitt[4]
        time = fullTime.split("&nbsp;&ndash;&nbsp;")
        startTime = time[0]
        endTime = time[1]
    else:
        a = False
        for s in splitt:
            if "&nbsp;&ndash;" in s:
                startTime = s.split("&nbsp;&ndash;")[0]
                a = True
        if a:
            endTime = splitt[8]
        else:
            startTime = "00:00AM"
            endTime = "11:59PM"

    return getDif(startTime, endTime)

"""
def getStart(obj):
    datex = getDate(parse(item['description']))
    splitt = datex.split(" ")
    if len(splitt) >= 4 and "&nbsp;&ndash;&nbsp;" in splitt[4]:
        fullTime = splitt[4]
        time = fullTime.split("&nbsp;&ndash;&nbsp;")
        startTime = time[0]
        endTime = time[1]
    else:
        a = False
        for s in splitt:
            if "&nbsp;&ndash;" in s:
                startTime = s.split("&nbsp;&ndash;")[0]
                a = True
        if a:
            endTime = splitt[8]
        else:
            startTime = "00:00AM"
            endTime = "11:59PM"

    return fixTime(startTime, endTime)

def getFeat(obj):
    feat = urllib.request.urlopen('http://25livepub.collegenet.com/calendars/featured-events-calendar-1.rss')
    data2 = feat.read()
    feat.close()

    data2 = xmltodict.parse(data2)
    itemsFeat = data2['rss']['channel']['item']

    h = False
    for f in itemsFeat:
        if (obj['title'] == f['title'] and obj['category'] == f['category']):
            h = True
    featured = h
    print("Featured = " + str(featured))"""

#def homepage(request):

file = urllib.request.urlopen('http://25livepub.collegenet.com/calendars/25live-all-events.rss')
data = file.read()
file.close()

data = xmltodict.parse(data)

items = data['rss']['channel']['item']

feat = urllib.request.urlopen('http://25livepub.collegenet.com/calendars/featured-events-calendar-1.rss')
data2 = feat.read()
feat.close()

data2 = xmltodict.parse(data2)
itemsFeat = data2['rss']['channel']['item']

DbRead()
ID = 9

for item in items:
    print("Title: " + item['title'])
    print("Date: " + item['category'])
    # Regex for Time
    title = getTitle(item)
    date = getDate(item)
    location = getLoc(item)
    description = getDescription(item)
    duration = getDuration(item)

    h = False
    for f in itemsFeat:
        if(item['title']==f['title'] and item['category']==f['category']):
            h = True
    featured = h
    print("Featured = " + str(featured))
    print()

    DbWrite(ID, title, description, location, date, "1:00", duration, featured)
    ID = ID + 1

DbRead()

print('Done');



