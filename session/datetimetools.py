from jdatetime import date, timedelta
import jdatetime
from django.utils import timezone


def AllSaturdays(length, start_time = jdatetime.datetime.now()):
   dates = date(start_time.year, start_time.month, start_time.day)    #today
   today = dates
   dates += timedelta(days = 0 - dates.weekday())
   current_month = start_time.month
   if 0 - today.weekday() >= 0:
       yield dates
   f = start_time + timedelta(days = length)
   try:
       f = f.date()
   except:
       f = f
   while dates <= f:
      dates += timedelta(days = 7)
      if dates <= f:
          yield dates


def AllSundays(length, start_time = jdatetime.datetime.now()):
   dates = date(start_time.year, start_time.month, start_time.day)    #today
   today = dates
   dates += timedelta(days = 1 - dates.weekday())
   current_month = start_time.month
   if 1 - today.weekday() >= 0:
       yield dates
   f = start_time + timedelta(days = length)
   try:
       f = f.date()
   except:
       f = f
   while dates <= f:
      dates += timedelta(days = 7)
      if dates <= f:
          yield dates


def AllMondays(length, start_time = jdatetime.datetime.now()):
   dates = date(start_time.year, start_time.month, start_time.day)    #today
   today = dates
   dates += timedelta(days = 2 - dates.weekday())
   current_month = start_time.month
   if 2 - today.weekday() >= 0:
       yield dates
   f = start_time + timedelta(days = length)
   try:
       f = f.date()
   except:
       f = f
   while dates <= f:
      dates += timedelta(days = 7)
      if dates <= f:
          yield dates


def AllTuesdays(length, start_time = jdatetime.datetime.now()):
   dates = date(start_time.year, start_time.month, start_time.day)    #today
   today = dates
   dates += timedelta(days = 3 - dates.weekday())
   current_month = start_time.month
   if 3 - today.weekday() >= 0:
       yield dates
   f = start_time + timedelta(days = length)
   try:
       f = f.date()
   except:
       f = f
   while dates <= f:
      dates += timedelta(days = 7)
      if dates <= f:
          yield dates


def AllWednesdays(length, start_time = jdatetime.datetime.now()):
   dates = date(start_time.year, start_time.month, start_time.day)    #today
   today = dates
   dates += timedelta(days = 4 - dates.weekday())
   current_month = start_time.month
   if 4 - today.weekday() >= 0:
       yield dates
   f = start_time + timedelta(days = length)
   try:
       f = f.date()
   except:
       f = f
   while dates <= f:
      dates += timedelta(days = 7)
      if dates <= f:
          yield dates


def AllThursdays(length, start_time = jdatetime.datetime.now()):
   dates = date(start_time.year, start_time.month, start_time.day)    #today
   today = dates
   dates += timedelta(days = 5 - dates.weekday())
   current_month = start_time.month
   if 5 - today.weekday() >= 0:
       yield dates
   f = start_time + timedelta(days = length)
   try:
       f = f.date()
   except:
       f = f
   while dates <= f:
      dates += timedelta(days = 7)
      if dates <= f:
          yield dates


def AllFridays(length, start_time = jdatetime.datetime.now()):
   dates = date(start_time.year, start_time.month, start_time.day)    #today
   today = dates
   dates += timedelta(days = 6 - dates.weekday())
   current_month = start_time.month
   if 6 - today.weekday() >= 0:
       yield dates
   f = start_time + timedelta(days = length)
   try:
       f = f.date()
   except:
       f = f
   while dates <= f:
      dates += timedelta(days = 7)
      if dates <= f:
          yield dates


def TotalMinutes(time):
    total_minutes = (time.hour * 60) + time.minute
    return total_minutes


'''
#string to date
from jdatetime import datetime as x

print(x.strptime('3:30 p.m.','%H:%M'))


dates = date(1398,10,20)
print(type(dates))
print(dates.weekday())

for day in AllThursdays(1):
    if day < jdatetime.datetime.now().date():
        print(day)
    else:
        print('sdasd')
'''
