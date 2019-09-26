from django import template
from django.shortcuts import get_object_or_404
from jdatetime import timedelta
from jdatetime import datetime as JDATETIMETOOL
from jdatetime import timedelta as jtimedelta
from booking.models import BookingModel
import jdatetime
import datetime
from jdatetime import date as jdate

register = template.Library()


from session.models import SessionModel, SessionCategoryModel

@register.filter(name='session_end')
def session_end(value):
    session = get_object_or_404(SessionModel,pk=value)
    duration = JDATETIMETOOL.strptime(session.duration,'%H:%M')
    session_end = duration + timedelta(hours = session.time.hour,
                                                    minutes = session.time.minute)
    if session_end.minute == 0:
        session_end_str = str(session_end.hour)+':'+str(session_end.minute)+'0'
    else:
        session_end_str = str(session_end.hour)+':'+str(session_end.minute)

    return session_end_str


@register.filter(name='ceil')
def ceil(pk):
    session_category = get_object_or_404(SessionCategoryModel,pk=pk)

    for existing_session in session_category.sessions.all():
                existing_duration = JDATETIMETOOL.strptime(existing_session.duration,'%H:%M')
                time_var = existing_duration + timedelta(hours = existing_session.time.hour,
                                                                minutes = existing_session.time.minute)
                try:
                    if time_var > ceil :
                        ceil = time_var

                except:
                    ceil = existing_duration +  timedelta(hours = existing_session.time.hour,
                                                                    minutes = existing_session.time.minute)

                try:
                    if JDATETIMETOOL.strptime(str(existing_session.time),'%H:%M') < floor:
                        floor = existing_session.time


                except:
                    floor = JDATETIMETOOL.strptime(str(existing_session.time),'%H:%M')
    try:

        return ceil.time
    except:
        return 2


@register.filter(name='floor')
def floor(pk):
    session_category = get_object_or_404(SessionCategoryModel,pk=pk)

    for existing_session in session_category.sessions.all():

                existing_duration = JDATETIMETOOL.strptime(existing_session.duration,'%H:%M')
                time_var = existing_duration + timedelta(hours = existing_session.time.hour,
                                                                minutes = existing_session.time.minute)
                try:
                    if time_var > ceil :
                        ceil = time_var

                except:
                    ceil = existing_duration +  timedelta(hours = existing_session.time.hour,
                                                                    minutes = existing_session.time.minute)

                try:
                    if JDATETIMETOOL.strptime(str(existing_session.time),'%H:%M') < floor:
                        floor = existing_session.time


                except:
                    floor = JDATETIMETOOL.strptime(str(existing_session.time),'%H:%M')
    try:

        return floor.time()
    except:
        return 2


@register.filter(name='duration')
def duration(pk):
    session_category = get_object_or_404(SessionCategoryModel,pk=pk)

    for existing_session in session_category.sessions.all():
        duration = existing_session.duration
        break
    try:

        return duration.time()
    except:
        return 2



@register.filter(name='final_price')
def final_price(value):
    session = get_object_or_404(SessionModel,pk=value)
    price = session.price
    final_price = (((100-session.discount_percentage)/100) * price ) * ((100 - session.salon.company_discount_percentage)/100)
    return final_price


@register.filter(name='pay_back_generator')
def pay_back_generator(value):
    today = jdatetime.datetime.now().date()
    now_time = datetime.datetime.now().time()

    booking_object = get_object_or_404(BookingModel, pk = value)
    session = booking_object.session
    ceil_date = jdate(today.year,today.month,today.day)+jtimedelta(days=2)
    ceil_time = (datetime.datetime.combine(datetime.date(1,1,1),now_time) + timedelta(hours = 5)).time()
    if booking_object.session.day >= ceil_date: # percent harm 3 for sportclub 2 for company
        if booking_object.is_contract:
            contract_discount = booking_object.contract_discount
            pay_back = (booking_object.final_price * (100-contract_discount-5))/100
        else:
            pay_back = booking_object.final_price * (95/100)

    elif booking_object.session.day == today and  booking_object.session.time < ceil_time:
        payback = False
    elif booking_object.session.day < today:
        payback = False
    else:
        if not booking_object.is_contract:
            pay_back = (booking_object.final_price * 85)/100
        else:
            contract_discount = booking_object.contract_discount
            pay_back = (booking_object.final_price * (85-contract_discount))/100
    return pay_back



@register.filter(name='the_past_day')
def the_past_day(value):
    day = value + timedelta(days=-1)
    return day

@register.filter(name='only_day')
def only_day(value):
    values = value.split('-')
    day = values[2]
    return day


@register.filter(name='cutbr')
def cutbr(value):
    value = value.replace('-br','')
    return value


@register.filter(name='only_month')
def only_month(value):
    values = value.split('-')
    month = values[1]
    if month == '1' :
        month = 'فروردین'
    if month == '2' :
        month = 'اردیبهشت'
    if month == '3' :
        month = 'خرداد'
    if month == '4' :
        month = 'تیر'
    if month == '5' :
        month = 'مرداد'
    if month == '6' :
        month = 'شهریور'
    if month == '7' :
        month = 'مهر'
    if month == '8' :
        month = 'آبان'
    if month == '9' :
        month = 'آذر'
    if month == '10' :
        month = 'دی'
    if month == '11' :
        month = 'بهمن'
    if month == '12' :
        month = 'اسفند'
    return month


@register.filter(name='only_year')
def only_year(value):
    values = value.split('-')
    year = values[0]
    return year
