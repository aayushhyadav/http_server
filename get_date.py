import datetime
import calendar

#returns the current day
def getday(date):
    day = datetime.datetime.strptime(date, '%d %m %Y').weekday() 
    return (calendar.day_name[day]) 

#returns the current month
def getMonth(mon):
    if mon == '01':
        return 'Jan'
    elif mon == '02':
        return 'Feb'
    elif mon == '03':
        return 'Mar'
    elif mon == '04':
        return 'Apr'
    elif mon == '05':
        return 'May'
    elif mon == '06':
        return 'Jun'
    elif mon == '07':
        return 'Jul'
    elif mon == '08':
        return 'Aug'
    elif mon == '09':
        return 'Sep'
    elif mon == '10':
        return 'Oct'
    elif mon == '11':
        return 'Nov'
    else:
        return 'Dec'

def getMonth_2(mon):
    if mon == 'Jan':
        return '01'
    elif mon == 'Feb':
        return '02'
    elif mon == 'Mar':
        return '03'
    elif mon == 'Apr':
        return '04'
    elif mon == 'May':
        return '05'
    elif mon == 'Jun':
        return '06'
    elif mon == 'Jul':
        return '07'
    elif mon == 'Aug':
        return '08'
    elif mon == 'Sep':
        return '09'
    elif mon == 'Oct':
        return '10'
    elif mon == 'Nov':
        return '11'
    else:
        return '12'