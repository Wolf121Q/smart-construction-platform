from core.models import User
import datetime,time,math, random

def Serial_increment(sn_number):
    if User.objects.filter(serial_number__icontains=sn_number).count() > 0:
        sn_number = int(sn_number)
        sn_number = sn_number + 1
        sn_number = str(sn_number)
        sn_number = Serial_increment(sn_number)
    return sn_number

def getSerialNumber():
    year = datetime.datetime.now().year
    month = datetime.datetime.now().month
    day = datetime.datetime.now().day
    member_count = User.objects.filter(created_on__year=year, created_on__month=month, created_on__day=day).count()
    if member_count == 0:
        member_count = 1
    member_count = str(member_count)
    s_number = member_count.rjust(6,'0')

    s_number = str(year)+str(month).rjust(2, '0')+str(day).rjust(2, '0')+str(s_number)
    s_number = Serial_increment(s_number)
    type = ""
    return str(type)+str(s_number)

