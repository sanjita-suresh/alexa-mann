import re
import datetime
import json
import ms_endpoints
import room_class
room = room_class.Room()

################################################################################
# Functions


# Amzazon Date: “today”: 2015-11-24
# Amazon Duration: “ten minutes”: PT10M, “five hours”: PT5H
# Amazon Time: “two fifteen pm”: 14:15
# MS DateTime: "2017-04-17T09:00:00",
# MS Duration : PT2H
def convert_amazon_to_ms(Date, Time):
    date_time = str(Date) + 'T' + str(Time)
    return date_time


def create_event_from_alexa(start, end, title, room_name, cal_id):
    """Handler for create_event route."""
    print("cal id:"+cal_id)
    ms_endpoints.call_createvent(room.token, start, end, title, room_name, cal_id)

def timeSum(timeA, timeB):
    hoursA = re.search(r'(^[^:]+)', timeA).group(1)
    minutesA = re.search(r'([^:]+$)', timeA).group(1)
    hoursB = re.search(r'(^[^:]+)', timeB).group(1)
    minutesB = re.search(r'([^:]+$)', timeB).group(1)

    minutes = (int(minutesA) + int(minutesB))
    if minutes > 60:
        extraHour = 1
        minutes = minutes % 60
    else:
        extraHour = 0

    hours = (extraHour + int(hoursA) + int(hoursB)) % 24

    if hours < 10:
        hours = "0" + str(hours)
    if minutes < 10:
        minutes = "0" + str(minutes)
    time = str(hours) + ":" + str(minutes)
    return time

def getMeetingEndTime(start, duration):
    if not re.search(r'\d\d:\d\d', start):
        start = start + ":00"
    if re.search(r'AF', start):
        if re.search(r'\b[1-9]\b', start):
            start = timeSum("0" + re.search(r'(\b[1-9]\b)', start).group(1) + ":00", "12:00")
        else:
            start = timeSum(re.search(r'(\d\d:\d\d)', start).group(1), "12:00")

    if re.search(r'\d*H', duration):
        hours = re.search(r'(\d*)H', duration).group(1)
    else:
        hours = '00'

    if re.search(r'\d*M', duration):
        minutes = re.search(r'(\d*)M', duration).group(1)
    else:
        minutes = '00'

    time = hours + ':' + minutes
    return timeSum(start, time)

# Check the right filepath
def store(data):
    with open('./resources/locationConstraint.json', 'w') as json_file:
        json_file.write(json.dumps(data))


def load():
    with open('./resources/locationConstraint.json') as json_file:
        data = json.load(json_file)
        return data


def create_room_to_json(isAvailable, city, country, postalCode, state, street, displayName, email, attendees):
    json_data = {
        "resolveAvailability": isAvailable,
        "address": {
            "city": city,
            "countryOrRegion": country,
            "postalCode": postalCode,
            "state": state,
            "street": street
        },
        "displayName": displayName,
        "locationEmailAddress": email,
        "maxAttendees": attendees
    }
    data = load()
    data['locations'].append(json_data)
    store(data)

load()

def delete_room_to_json(name):
    data=load()
    x=0
    for i in range(0, len(data['locations'])):
        if(data['locations'][i]['displayName']==name ):
            print("find it")
            x=i
        else:
            print("not find")

    data['locations'].pop(x)
    store(data)

