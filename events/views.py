import datetime
from django.shortcuts import render

def EscapeRoomIndexView(request): 
    daylist =[
        {"id":1 ,"date": 1552901400000, "availability": 0},
        {"id":2 ,"date": 1552919400000, "availability": 0},
        {"id":3 ,"date": 1552987800000, "availability": 0},
        {"id":4 ,"date": 1553005800000, "availability": 0},
        {"id":5 ,"date": 1553074200000, "availability": 0},
        {"id":6 ,"date": 1553092200000, "availability": 0},
        {"id":7 ,"date": 1553160600000, "availability": 0},
        {"id":8 ,"date": 1553178600000, "availability": 0}
    ]
    
    escape_room_days = []
    last_day = ""
    for event in daylist:
        date = datetime.datetime.fromtimestamp(event["date"]/1000.0)
        if(last_day != date.strftime("%A")):
            escape_room_days.append([])
        escape_room_days[-1].append(event)

        ## Delete this line when adding sql
        escape_room_days[-1][-1]["date"] = datetime.datetime.fromtimestamp(escape_room_days[-1][-1]["date"]/1000.0)

        last_day = date.strftime("%A")

    # Remove events with availability 0
    escape_room_days = list(map(lambda x : list(filter(lambda y : y["availability"]>0, x)), escape_room_days))

    # Remove days without events
    escape_room_days = list(filter(lambda x : len(x) != 0,escape_room_days))

    template_name = 'events/escape-room.html'
    return render(request, template_name, context={"escape_room_days":escape_room_days})