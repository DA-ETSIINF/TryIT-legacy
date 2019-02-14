import datetime
from django.shortcuts import render

def EscapeRoomIndexView(request): 
    # daylist must be sorted by date!!!
    daylist =[
        {"id":1 ,"date": 1552901400000, "availability": 10},
        {"id":2 ,"date": 1552919400000, "availability": 20},
        {"id":3 ,"date": 1552987800000, "availability": 10},
        {"id":4 ,"date": 1553005800000, "availability": 20},
        {"id":5 ,"date": 1553074200000, "availability": 10},
        {"id":6 ,"date": 1553092200000, "availability": 10},
        {"id":7 ,"date": 1553160600000, "availability": 10},
        {"id":8 ,"date": 1553178600000, "availability": 10}
    ]
    
    '''
    We need to transform daylist in array (which each element represent a day)
    of array (which each element is an event of that day). At the end, we will have 
    something similar to:
    escape_room_days = [
        // monday
        [
            { id: number, date: Date, availability: number},
            ...
        ],

        // tuesday
        [
            { id: number, date: Date, availability: number},
            ...
        ],
        ...
    ]
    '''

    # Final list
    escape_room_days = []

    for i, event in enumerate(daylist):
        # Convert number to date
        # may not be necessary when adding sql sentence
        event["date"] = datetime.datetime.fromtimestamp(event["date"]/1000.0)

        # Detect if the day of event is the same as the previous event in the array.
        if(i == 0 or daylist[i - 1]["date"].strftime("%A") != event["date"].strftime("%A")):
            # If is not the same day, then we create another day, which is an empty array
            escape_room_days.append([])
        
        # Add the event to the last array
        escape_room_days[-1].append(event)


    # Remove events with availability 0
    escape_room_days = list(map(lambda x : list(filter(lambda y : y["availability"]>0, x)), escape_room_days))

    # Remove days without events
    escape_room_days = list(filter(lambda x : len(x) != 0,escape_room_days))

    template_name = 'events/escape-room.html'
    return render(request, template_name, context={"escape_room_days":escape_room_days})