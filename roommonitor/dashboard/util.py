import re
import datetime
import json
import ms_endpoints
import room_class
import urllib
import ssl
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


def getMeetingEndTime(start, duration):

    if re.search(r'\d*H', duration):
        hours = re.search(r'(\d*)H', duration).group(1)
    else:
        hours = '00'

    if re.search(r'\d*M', duration):
        minutes = re.search(r'(\d*)M', duration).group(1)
    else:
        minutes = '00'

    time = hours + ':' + minutes

    timeList = [start, time]
    sum = datetime.timedelta()
    for i in timeList:
        (h, m) = i.split(':')
        d = datetime.timedelta(hours=int(h), minutes=int(m))
        sum += d

    if len(str(sum)) < 8:
        return  '0' + str(sum)
    return str(sum)

print(getMeetingEndTime("16:00", "PT3H4M"))


# Check the right filepath
def store(data):
    #with open('./resources/locationConstraint.json', 'w') as json_file:
    #   json_file.write(json.dumps(data))
    #print(data)
    '''
    headers = {'content-type': 'application/json'}
    url = "https://sovanta.ddnss.de/locationConstraint.json"
    requests.post(url, data=json.dumps(data), headers=headers, verify=False)
    '''
    ctx = ssl.create_default_context()
    ctx.check_hostname = False
    ctx.verify_mode = ssl.CERT_NONE
    url = "https://sovanta.ddnss.de/locationConstraint"
    req = urllib.request.Request(url)
    req.add_header('Content-Type', 'application/json; charset=utf-8')
    jsondata = json.dumps(data)
    jsondataasbytes = jsondata.encode('utf-8')  # needs to be bytes
    req.add_header('Content-Length', len(jsondataasbytes))
    req.get_method = lambda: 'POST'
    print(jsondataasbytes)
    response = urllib.request.urlopen(url, jsondataasbytes, context=ctx)
    print(response)





def load():
    #with open('./resources/locationConstraint.json') as json_file:
        #url = "https://sovanta.ddnss.de/locationConstraint.json"
        #data = json.load(json_file)
    ctx = ssl.create_default_context()
    ctx.check_hostname = False
    ctx.verify_mode = ssl.CERT_NONE
    with urllib.request.urlopen("https://sovanta.ddnss.de/locationConstraint.json",context=ctx) as url:
        data = json.loads(url.read().decode())
        print(data)
        return data
    #url = 'https://sovanta.ddnss.de/locationConstraint.json'
    #req = urllib.request.get(url,{'Content-Type': 'application/json'},verify=False)
    #data = urllib.urlopen(req)
    #url = 'https://sovanta.ddnss.de/locationConstraint.json'
    #headers = {'content-type': 'application/json'}
    #data=requests.get(url, data=json.load(), headers=headers)
    #return data


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