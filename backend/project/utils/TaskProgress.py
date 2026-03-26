import datetime

def CalculateProgressMonth(start_date, end_date):
    if start_date and end_date:
        start_date, end_date
        today = datetime.datetime.now().date()
        progress = 0
        # if type(today) is datetime.date:
        #     today = datetime.datetime.combine(today, datetime.datetime.min.time())
        # today = datetime.datetime.now()
        if today <= start_date:
            progress = 0
        elif today >= end_date:
            progress = 100
        else:
            duration = calculate_date_diff_in_days(start_date, end_date)

            if duration != 0:
                progress = (calculate_date_diff_in_days(start_date, today) / calculate_date_diff_in_days(start_date,end_date)) * 100
        return round(progress, 2)
    else:
        return 0

def calculate_date_diff_in_days(act_startdate, act_enddate):
    duration = act_enddate - act_startdate
    return duration.days