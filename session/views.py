from django.shortcuts import render
from django.views.generic import CreateView, TemplateView, UpdateView, ListView
from django.shortcuts import get_object_or_404, get_list_or_404
from jdatetime import date, timedelta
from jdatetime import datetime as JDATETIMETOOL
from datetime import datetime as DATETIMETOOL
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
import jdatetime
import datetime
from django.http import HttpResponseRedirect
from django.urls import reverse, reverse_lazy
from django.core.paginator import Paginator

#handmade
from session.forms import (DaysForm, TimesForm, PriceForm, SessionDeleteForm,
                            DaysForm_2, LastDataSetForm, DiscountPercentageForm,
                            StatusForm,)
from session.models import (SessionModel, LastDataModel, SessionCategoryModel)
from salon.models import SalonModel
from masteruser.decorators import masteruser_required
from sportclub.decorators import sportclub_required
from commonuser.decorators import commonuser_required
from session.filters import SessionFilter
from session.datetimetools import (AllSaturdays, AllSundays, AllMondays,
                                AllTuesdays, AllWednesdays, AllThursdays,
                                AllFridays, TotalMinutes)




@login_required
@sportclub_required
def SessionWorkSpaceView(request,pk):
    salon = get_object_or_404(SalonModel,pk = pk)
    if request.user == salon.sportclub.user:
        ### creating days

        from jdatetime import date as jdate
        ##################################################################################################### 0
        now = jdatetime.datetime.now()
        if now.month == 12:
            month_length =  (jdate(now.year+1, 1, 1) - jdate(now.year, 12, 1)).days
            previous_month_length = (jdate(now.year, now.month, 1) - jdate(now.year, now.month-1, 1)).days
            this_date = str(now.year)+'-12-'
            next_date = str(now.year+1)+'-1-'
            prev_date = str(now.year)+'-11-'
        elif now.month == 1:
            month_length =  (jdate(now.year, now.month+1, 1) - jdate(now.year, now.month, 1)).days
            previous_month_length = (jdate(now.year, now.month, 1) - jdate(now.year-1, 12, 1)).days
            this_date = str(now.year)+'-1-'
            next_date = str(now.year)+'-2-'
            prev_date = str(now.year-1)+'-12-'
        else:
            month_length =  (jdate(now.year, now.month+1, 1) - jdate(now.year, now.month, 1)).days
            previous_month_length = (jdate(now.year, now.month, 1) - jdate(now.year, now.month-1, 1)).days
            this_date = str(now.year)+'-'+str(now.month)+'-'
            next_date = str(now.year)+'-'+str(now.month+1)+'-'
            prev_date = str(now.year)+'-'+str(now.month-1)+'-'

        first_day_of_month_weekday = jdate(now.year, now.month, 1).weekday()
        array = [0,]
        days_1 = [0,]
        if (month_length == 30 and first_day_of_month_weekday == 6) or (month_length == 31 and first_day_of_month_weekday >=5):
            for i in range(41):
                array.append(0)
                days_1.append(0)
        else:
            for i in range(34):
                array.append(0)
                days_1.append(0)


        for i in range(first_day_of_month_weekday):
            array[first_day_of_month_weekday-i-1] = prev_date + '' #str(previous_month_length - i)

        for i in range(month_length):
            array[first_day_of_month_weekday+i] = this_date + str(i + 1)

        for i in range(len(array) - array.index(0)):
            array[array.index(0)] = next_date+ '' #str(i+1)
        for i in range(len(array)):
            days_1[i] = array[(int(i/7)+1)*7-1-(i-int(i/7)*7)]
        for i in range(len(days_1)):
            if int((i)/7) == ((i)/7):
                days_1[i] = days_1[i]+'-br'
        now = jdatetime.datetime.now().date()

        return render(request,'session/workspace.html',
                          {'salon':salon,'days_1':days_1,'now':now})
    else:
        return HttpResponseRedirect(reverse('login'))



@login_required
def SessionListView(request,pk):
    from jdatetime import date as jdate
    salon_instance = get_object_or_404(SalonModel,pk = pk)
    if request.user == salon_instance.sportclub.user or request.user.is_masteruser:
        sessions = get_list_or_404(SessionModel.objects.order_by('day'),salon = salon_instance)

        first_day = sessions[0].day
        last_day = sessions[-1].day

        counter = 0
        while True:
            if counter == 0:
                now = first_day
                if now.month == 12:
                    month_length =  (jdate(now.year+1, 1, 1) - jdate(now.year, 12, 1)).days
                    previous_month_length = (jdate(now.year, now.month, 1) - jdate(now.year, now.month-1, 1)).days
                    this_date = str(now.year)+'-12-'
                    next_date = str(now.year+1)+'-1-'
                    prev_date = str(now.year)+'-11-'
                elif now.month == 1:
                    month_length =  (jdate(now.year, now.month+1, 1) - jdate(now.year, now.month, 1)).days
                    previous_month_length = (jdate(now.year, now.month, 1) - jdate(now.year-1, 12, 1)).days
                    this_date = str(now.year)+'-1-'
                    next_date = str(now.year)+'-2-'
                    prev_date = str(now.year-1)+'-12-'
                else:
                    month_length =  (jdate(now.year, now.month+1, 1) - jdate(now.year, now.month, 1)).days
                    previous_month_length = (jdate(now.year, now.month, 1) - jdate(now.year, now.month-1, 1)).days
                    this_date = str(now.year)+'-'+str(now.month)+'-'
                    next_date = str(now.year)+'-'+str(now.month+1)+'-'
                    prev_date = str(now.year)+'-'+str(now.month-1)+'-'

                first_day_of_month_weekday = jdate(now.year, now.month, 1).weekday()
                array = [0,]
                days = [0,]
                if (month_length == 30 and first_day_of_month_weekday == 6) or (month_length == 31 and first_day_of_month_weekday >=5):
                    for i in range(41):
                        array.append(0)
                        days.append(0)
                else:
                    for i in range(34):
                        array.append(0)
                        days.append(0)


                for i in range(first_day_of_month_weekday):
                    array[first_day_of_month_weekday-i-1] = prev_date + '' #str(previous_month_length - i)

                for i in range(month_length):
                    array[first_day_of_month_weekday+i] = this_date + str(i + 1)

                for i in range(len(array) - array.index(0)):
                    array[array.index(0)] = next_date+ '' #str(i+1)
                for i in range(len(array)):
                    days[i] = array[(int(i/7)+1)*7-1-(i-int(i/7)*7)]
                for i in range(len(days)):
                    if int((i)/7) == ((i)/7):
                        days[i] = days[i]+'-br'
                dictionary = {'days_0':days,}
                counter = 1
                if now.year == last_day.year and now.month == last_day.month:
                    break
            else:
                now = jdate(now.year,now.month,15)+timedelta(days=30)
                if now.month == 12:
                    month_length =  (jdate(now.year+1, 1, 1) - jdate(now.year, 12, 1)).days
                    previous_month_length = (jdate(now.year, now.month, 1) - jdate(now.year, now.month-1, 1)).days
                    this_date = str(now.year)+'-12-'
                    next_date = str(now.year+1)+'-1-'
                    prev_date = str(now.year)+'-11-'
                elif now.month == 1:
                    month_length =  (jdate(now.year, now.month+1, 1) - jdate(now.year, now.month, 1)).days
                    previous_month_length = (jdate(now.year, now.month, 1) - jdate(now.year-1, 12, 1)).days
                    this_date = str(now.year)+'-1-'
                    next_date = str(now.year)+'-2-'
                    prev_date = str(now.year-1)+'-12-'
                else:
                    month_length =  (jdate(now.year, now.month+1, 1) - jdate(now.year, now.month, 1)).days
                    previous_month_length = (jdate(now.year, now.month, 1) - jdate(now.year, now.month-1, 1)).days
                    this_date = str(now.year)+'-'+str(now.month)+'-'
                    next_date = str(now.year)+'-'+str(now.month+1)+'-'
                    prev_date = str(now.year)+'-'+str(now.month-1)+'-'

                first_day_of_month_weekday = jdate(now.year, now.month, 1).weekday()
                array = [0,]
                days = [0,]
                if (month_length == 30 and first_day_of_month_weekday == 6) or (month_length == 31 and first_day_of_month_weekday >=5):
                    for i in range(41):
                        array.append(0)
                        days.append(0)
                else:
                    for i in range(34):
                        array.append(0)
                        days.append(0)


                for i in range(first_day_of_month_weekday):
                    array[first_day_of_month_weekday-i-1] = prev_date + '' #str(previous_month_length - i)

                for i in range(month_length):
                    array[first_day_of_month_weekday+i] = this_date + str(i + 1)

                for i in range(len(array) - array.index(0)):
                    array[array.index(0)] = next_date+ '' #str(i+1)
                for i in range(len(array)):
                    days[i] = array[(int(i/7)+1)*7-1-(i-int(i/7)*7)]
                for i in range(len(days)):
                    if int((i)/7) == ((i)/7):
                        days[i] = days[i]+'-br'
                dictionary['days_{first}'.format(first = str(counter))] = days
                counter += 1
                if now.year == last_day.year and now.month == last_day.month:
                    break
        session_days=['',]
        i=0
        for session in sessions:
            str_1 = str(session.day)
            str_1 = str_1.replace('-0','-',2)
            session_days.append(str_1)
        return render(request,'session/sessionlist.html',{'data': sorted(dictionary.items()),'session_days':session_days,'salon':salon_instance})
    else:
        return HttpResponseRedirect(reverse('login'))


class LengthError(TemplateView):
    template_name = 'session/lengtherror.html'


@login_required
@sportclub_required
def SessionCategoriesView(request,pk):
    salon = get_object_or_404(SalonModel,pk = pk)
    if request.user == salon.sportclub.user:
        sessioncategory_instances = get_list_or_404(SessionCategoryModel, salon = salon)
        return render(request, 'session/categories.html',
                    {'categories':sessioncategory_instances,'salon':salon})
    return HttpResponseRedirect(reverse('login'))


@login_required
@sportclub_required
def SetPriceView(request,pk):
    sessioncategory_instance = get_object_or_404(SessionCategoryModel,pk = pk)
    if sessioncategory_instance.salon.sportclub.user == request.user:
        if request.method == "POST":
            checks = request.POST.getlist('checks')
            days = request.POST.getlist('days')
            price_form = PriceForm(data = request.POST )
            if price_form.is_valid():
                range_start_str = price_form.cleaned_data['range_start']
                range_start_list = range_start_str.split('-')
                range_start = jdatetime.date(int(range_start_list[0]),int(range_start_list[1]),int(range_start_list[2]))
                range_end_str = price_form.cleaned_data['range_end']
                range_end_list = range_end_str.split('-')
                range_end = jdatetime.date(int(range_end_list[0]),int(range_end_list[1]),int(range_end_list[2]))
                price = price_form.cleaned_data['price']
                sessioncategory_instance = get_object_or_404(SessionCategoryModel,pk = pk)
                today = jdatetime.datetime.now().date()
                if today > range_start or len(checks) == 0 or sessioncategory_instance.range_start_day > range_start or range_start > range_end or sessioncategory_instance.range_end_day < range_end :
                    return HttpResponseRedirect(reverse('session:logicalerror'))
                sessions = sessioncategory_instance.sessions.all()
                for session in sessions:
                    x1 = session.day - range_start
                    x2 = session.day - range_end
                    if int(x1.days) >= 0 and int(x2.days) <= 0 :
                        if str(session.day.weekday()) in days:
                            for check in checks:
                                check_time = DATETIMETOOL.strptime(check,'%H:%M')
                                check_time = check_time.time()
                                if session.time.minute - check_time.minute == 0 and session.time.hour - check_time.hour == 0:
                                    if not session.is_booked:
                                        session.price = price
                                        session.is_ready = True
                                        session.save()
                #for reverse
                salon_pk = sessioncategory_instance.salon.pk
                return HttpResponseRedirect(reverse('session:workspace',
                                                    kwargs={'pk':salon_pk}))

        else:
            price_form = PriceForm()
            list = sessioncategory_instance.sessions.all()
            obj = list[0]
            session_instances = get_list_or_404(SessionModel,day = obj.day,
                                                session_category = sessioncategory_instance)
        today = jdatetime.datetime.now().date()
        return render(request,'session/setprice.html',{'sessions':session_instances,
                      'session_category':sessioncategory_instance,'form':price_form,
                      'today':today})
    else:
        return HttpResponseRedirect(reverse('login'))


@login_required
@sportclub_required
def SetDiscountPercentageView(request,pk):
    sessioncategory_instance = get_object_or_404(SessionCategoryModel,pk = pk)
    if sessioncategory_instance.salon.sportclub.user == request.user:
        if request.method == "POST":
            checks = request.POST.getlist('checks')
            days = request.POST.getlist('days')
            discount_percentage_form = DiscountPercentageForm(data = request.POST )
            if discount_percentage_form.is_valid():
                range_start_str = discount_percentage_form.cleaned_data['range_start']
                range_start_list = range_start_str.split('-')
                range_start = jdatetime.date(int(range_start_list[0]),int(range_start_list[1]),int(range_start_list[2]))
                range_end_str = discount_percentage_form.cleaned_data['range_end']
                range_end_list = range_end_str.split('-')
                range_end = jdatetime.date(int(range_end_list[0]),int(range_end_list[1]),int(range_end_list[2]))
                discount_percentage = discount_percentage_form.cleaned_data['discount_percentage']
                sessioncategory_instance = get_object_or_404(SessionCategoryModel,pk = pk)
                today = jdatetime.datetime.now().date()
                if today > range_start or discount_percentage > 100 or len(checks) == 0 or sessioncategory_instance.range_start_day > range_start or range_start > range_end or sessioncategory_instance.range_end_day < range_end :
                    return HttpResponseRedirect(reverse('session:logicalerror'))
                sessions = sessioncategory_instance.sessions.all()
                for session in sessions:
                    x1 = session.day - range_start
                    x2 = session.day - range_end
                    if int(x1.days) >= 0 and int(x2.days) <= 0 :
                        if str(session.day.weekday()) in days:
                            for check in checks:
                                check_time = DATETIMETOOL.strptime(check,'%H:%M')
                                check_time = check_time.time()
                                if session.time.minute - check_time.minute == 0 and session.time.hour - check_time.hour == 0:
                                    if not session.is_booked:
                                        session.discount_percentage = discount_percentage
                                        session.save()
                #for reverse
                salon_pk = sessioncategory_instance.salon.pk
                return HttpResponseRedirect(reverse('session:workspace',
                                                    kwargs={'pk':salon_pk}))

        else:
            discount_percentage_form = DiscountPercentageForm()
            list = sessioncategory_instance.sessions.all()
            obj = list[0]
            session_instances = get_list_or_404(SessionModel,day = obj.day,
                                                session_category = sessioncategory_instance)
        today = jdatetime.datetime.now().date()
        return render(request,'session/setdiscountpercentage.html',{'sessions':session_instances,
                      'session_category':sessioncategory_instance,'form':discount_percentage_form,
                      'today':today})
    else:
        return HttpResponseRedirect(reverse('login'))


@login_required
@sportclub_required
def StatusChangeView(request,pk):
    sessioncategory_instance = get_object_or_404(SessionCategoryModel,pk = pk)
    if sessioncategory_instance.salon.sportclub.user == request.user:
        if request.method == "POST":
            checks = request.POST.getlist('checks')
            days = request.POST.getlist('days')
            status_form = StatusForm(data = request.POST )
            is_ready = request.POST.get('is_ready')
            if status_form.is_valid():
                range_start_str = status_form.cleaned_data['range_start']
                range_start_list = range_start_str.split('-')
                range_start = jdatetime.date(int(range_start_list[0]),int(range_start_list[1]),int(range_start_list[2]))
                range_end_str = status_form.cleaned_data['range_end']
                range_end_list = range_end_str.split('-')
                range_end = jdatetime.date(int(range_end_list[0]),int(range_end_list[1]),int(range_end_list[2]))
                sessioncategory_instance = get_object_or_404(SessionCategoryModel,pk = pk)
                today = jdatetime.datetime.now().date()
                if today > range_start or sessioncategory_instance.range_start_day > range_start or range_start > range_end or sessioncategory_instance.range_end_day < range_end :
                    return HttpResponseRedirect(reverse('session:logicalerror'))
                sessions = sessioncategory_instance.sessions.all()
                for session in sessions:
                    x1 = session.day - range_start
                    x2 = session.day - range_end
                    if int(x1.days) >= 0 and int(x2.days) <= 0 :
                        if str(session.day.weekday()) in days:
                            for check in checks:
                                check_time = DATETIMETOOL.strptime(check,'%H:%M')
                                check_time = check_time.time()
                                if session.time.minute - check_time.minute == 0 and session.time.hour - check_time.hour == 0:
                                    if not session.is_booked:
                                        if is_ready == 'true':
                                            if session.price:
                                                session.is_ready == True
                                                session.save()
                                        else:
                                            session.is_ready = False
                                            session.save()

                #for reverse
                salon_pk = sessioncategory_instance.salon.pk
                return HttpResponseRedirect(reverse('session:workspace',
                                                    kwargs={'pk':salon_pk}))
            else:
                print(status_form.errors)

        else:
            status_form = StatusForm()
            list = sessioncategory_instance.sessions.all()
            obj = list[0]
            session_instances = get_list_or_404(SessionModel,day = obj.day,
                                                session_category = sessioncategory_instance)
        today = jdatetime.datetime.now().date()
        status_form = StatusForm()
        list = sessioncategory_instance.sessions.all()
        obj = list[0]
        session_instances = get_list_or_404(SessionModel,day = obj.day,
                                            session_category = sessioncategory_instance)
        return render(request,'session/statuschange.html',{'sessions':session_instances,
                      'session_category':sessioncategory_instance,'form':status_form,
                      'today':today})
    else:
        return HttpResponseRedirect(reverse('login'))



def CategorizedSessionListView(request,pk):
    sessioncategory_instance = get_object_or_404(SessionCategoryModel,pk = pk)
    session_list = SessionModel.objects.filter(session_category = sessioncategory_instance).order_by('day','time')
    session_filter = SessionFilter(request.GET,queryset = session_list)
    paginator = Paginator(session_filter.qs, 20)
    page = request.GET.get('page')
    sessions = paginator.get_page(page)
    now = jdatetime.datetime.now().date()
    now_time = jdatetime.datetime.now().time()
    return render(request,'session/categorizedsessionlist.html',{'sessions':sessions,
                  'filter':session_filter,'now':now,'now_time':now_time,
                  'session_category':sessioncategory_instance,})


@method_decorator([login_required, sportclub_required], name='dispatch')
class SessionUpdateView(UpdateView):
    model = SessionModel
    fields = ['is_ready','price','discount_percentage',]
    template_name = 'session/sessionupdate.html'

    def form_valid(self, form):
        today = jdatetime.datetime.now().date()
        if self.object.day < today:
            return super(SessionUpdateView, self).form_invalid(form)
        if form.cleaned_data['discount_percentage'] > 100:
            return super(SessionUpdateView, self).form_invalid(form)
        if form.cleaned_data['is_ready']:
            if not self.object.price:
                 return super(SessionUpdateView, self).form_invalid(form)
        if self.object.is_booked:
            return super(SessionUpdateView, self).form_invalid(form)
        self.object = form.save()
        return super().form_valid(form)

    def get_queryset(self):
        pk = self.kwargs.get(self.pk_url_kwarg)
        obj = get_object_or_404(SessionModel,pk = pk)
        if obj.salon.sportclub.user == self.request.user:
            return self.model._default_manager.all()

    def get_success_url(self):
        pk = self.object.session_category.salon.pk
        return reverse('session:workspace', kwargs={'pk':pk})



@login_required
@sportclub_required
def SessionDeleteView(request,pk):
    sessioncategory_instance = get_object_or_404(SessionCategoryModel,pk = pk)
    if sessioncategory_instance.salon.sportclub.user == request.user:
        if request.method == "POST":
            checks = request.POST.getlist('checks')
            days = request.POST.getlist('days')
            form = SessionDeleteForm(data = request.POST )
            if form.is_valid():
                range_start_str = form.cleaned_data['range_start']
                range_start_list = range_start_str.split('-')
                range_start = jdatetime.date(int(range_start_list[0]),int(range_start_list[1]),int(range_start_list[2]))
                range_end_str = form.cleaned_data['range_end']
                range_end_list = range_end_str.split('-')
                range_end = jdatetime.date(int(range_end_list[0]),int(range_end_list[1]),int(range_end_list[2]))
                sessions = sessioncategory_instance.sessions.all()
                ########## chekc if deleting doesn't start from range start day
                today = jdatetime.datetime.now().date()
                if today > range_start or sessioncategory_instance.range_start_day > range_start or range_start > range_end or sessioncategory_instance.range_end_day < range_end :
                    return HttpResponseRedirect(reverse('session:logicalerror'))

                for session in sessions:
                    x1 = session.day - range_start
                    x2 = session.day - range_end
                    x3 = session.day - sessioncategory_instance.range_start_day
                    x4 = session.day - sessioncategory_instance.range_end_day
                    if int(x1.days) >= 0 and int(x2.days) <= 0 :
                        if str(session.day.weekday()) in days:
                            for check in checks:
                                check_time = DATETIMETOOL.strptime(check,'%H:%M')
                                check_time = check_time.time()
                                if session.time.minute - check_time.minute == 0 and session.time.hour - check_time.hour == 0:
                                    if session.is_booked:
                                        return HttpResponseRedirect(reverse('session:is_booked'))

                if range_start != sessioncategory_instance.range_start_day:
                    session_category_1 = SessionCategoryModel.objects.create(salon=sessioncategory_instance.salon,
                                            range_start_day = sessioncategory_instance.range_start_day,
                                            range_end_day = range_start+timedelta(days=-1))
                    session_category_1.save()
                if range_end != sessioncategory_instance.range_end_day:
                    session_category_2 = SessionCategoryModel.objects.create(salon=sessioncategory_instance.salon,
                                            range_start_day = range_end+timedelta(days=1),
                                            range_end_day = sessioncategory_instance.range_end_day)
                    session_category_2.save()
                session_category_3 = SessionCategoryModel.objects.create(salon=sessioncategory_instance.salon,
                                        range_start_day = range_start,
                                        range_end_day = range_end)
                session_category_3.save()
                session_category_4 = SessionCategoryModel.objects.create(salon=sessioncategory_instance.salon,
                                        range_start_day = range_start,
                                        range_end_day = range_end)
                session_category_4.save()
                ###########
                for session in sessions:
                    x1 = session.day - range_start
                    x2 = session.day - range_end
                    x3 = session.day - sessioncategory_instance.range_start_day
                    x4 = session.day - sessioncategory_instance.range_end_day
                    if int(x3.days) >= 0 and int(x1.days) < 0 :
                        if session.day.weekday() == 0:
                            session_category_1.saturdays = True
                            session_category_1.save()
                        if session.day.weekday() == 1:
                            session_category_1.sundays = True
                            session_category_1.save()
                        if session.day.weekday() == 2:
                            session_category_1.mondays = True
                            session_category_1.save()
                        if session.day.weekday() == 3:
                            session_category_1.tuesdays = True
                            session_category_1.save()
                        if session.day.weekday() == 4:
                            session_category_1.wednesdays = True
                            session_category_1.save()
                        if session.day.weekday() == 5:
                            session_category_1.thursdays = True
                            session_category_1.save()
                        if session.day.weekday() == 6:
                            session_category_1.fridays = True
                            session_category_1.save()
                        session.session_category = session_category_1
                        session.save()
                    if int(x1.days) >= 0 and int(x2.days) <= 0 :
                        if str(session.day.weekday()) in days:
                            for check in checks:
                                check_time = DATETIMETOOL.strptime(check,'%H:%M')
                                check_time = check_time.time()
                                if session.time.minute - check_time.minute == 0 and session.time.hour - check_time.hour == 0:
                                    session.delete()
                    if int(x2.days) > 0 and int(x4.days) <= 0 :
                        if session.day.weekday() == 0:
                            session_category_2.saturdays = True
                            session_category_2.save()
                        if session.day.weekday() == 1:
                            session_category_2.sundays = True
                            session_category_2.save()
                        if session.day.weekday() == 2:
                            session_category_2.mondays = True
                            session_category_2.save()
                        if session.day.weekday() == 3:
                            session_category_2.tuesdays = True
                            session_category_2.save()
                        if session.day.weekday() == 4:
                            session_category_2.wednesdays = True
                            session_category_2.save()
                        if session.day.weekday() == 5:
                            session_category_2.thursdays = True
                            session_category_2.save()
                        if session.day.weekday() == 6:
                            session_category_2.fridays = True
                            session_category_2.save()
                        session.session_category = session_category_2
                        session.save()

                for session_1 in sessioncategory_instance.sessions.all():
                    if str(session_1.day.weekday()) in days:
                        if session_1.day.weekday() == 0:
                            session_category_3.saturdays = True
                            session_category_3.save()
                        if session_1.day.weekday() == 1:
                            session_category_3.sundays = True
                            session_category_3.save()
                        if session_1.day.weekday() == 2:
                            session_category_3.mondays = True
                            session_category_3.save()
                        if session_1.day.weekday() == 3:
                            session_category_3.tuesdays = True
                            session_category_3.save()
                        if session_1.day.weekday() == 4:
                            session_category_3.wednesdays = True
                            session_category_3.save()
                        if session_1.day.weekday() == 5:
                            session_category_3.thursdays = True
                            session_category_3.save()
                        if session_1.day.weekday() == 6:
                            session_category_3.fridays = True
                            session_category_3.save()
                        session_1.session_category = session_category_3
                        session_1.save()
                    else:
                        if session_1.day.weekday() == 0:
                            session_category_4.saturdays = True
                            session_category_4.save()
                        if session_1.day.weekday() == 1:
                            session_category_4.sundays = True
                            session_category_4.save()
                        if session_1.day.weekday() == 2:
                            session_category_4.mondays = True
                            session_category_4.save()
                        if session_1.day.weekday() == 3:
                            session_category_4.tuesdays = True
                            session_category_4.save()
                        if session_1.day.weekday() == 4:
                            session_category_4.wednesdays = True
                            session_category_4.save()
                        if session_1.day.weekday() == 5:
                            session_category_4.thursdays = True
                            session_category_4.save()
                        if session_1.day.weekday() == 6:
                            session_category_4.fridays = True
                            session_category_4.save()
                        session_1.session_category = session_category_4
                        session_1.save()
                if len(session_category_3.sessions.all()) == 0:
                    session_category_3.delete()
                if len(session_category_4.sessions.all()) == 0:
                    session_category_4.delete()

                #for reverse
                salon_pk = sessioncategory_instance.salon.pk
                sessioncategory_instance.delete()
                return HttpResponseRedirect(reverse('session:workspace',
                                                    kwargs={'pk':salon_pk}))
            else:
                print(form.errors)

        else:
            form = SessionDeleteForm()
            list = sessioncategory_instance.sessions.all()
            obj = list[0]
            session_instances = get_list_or_404(SessionModel,day = obj.day,
                                                session_category = sessioncategory_instance)
        today = jdatetime.datetime.now().date()
        return render(request,'session/sessiondelete.html',{'sessions':session_instances,
                      'session_category':sessioncategory_instance,'form':form,
                      'today':today})
    else:
        return HttpResponseRedirect(reverse('login'))


@login_required
@sportclub_required
def SessionCreateView_2(request,pk):
    salon_instance = get_object_or_404(SalonModel, pk = pk)
    last_data_instance = get_object_or_404(LastDataModel,salon = salon_instance)
    if salon_instance.sportclub.user == request.user:

        if request.method == 'POST':
            selected_days = request.POST.getlist('selected_days')
            days_form_2 = DaysForm_2(data = request.POST )
            times_form = TimesForm(data = request.POST )
            if times_form.is_valid() and days_form_2.is_valid():

                first_day_str = days_form_2.cleaned_data['first_day']
                first_day_list = first_day_str.split('-')
                first_day = jdatetime.date(int(first_day_list[0]),int(first_day_list[1]),int(first_day_list[2]))
                #last_day is treating as final day (last_day is sessioning :) )
                last_day_str = days_form_2.cleaned_data['last_day']
                last_day_list = last_day_str.split('-')
                last_day = jdatetime.date(int(last_day_list[0]),int(last_day_list[1]),int(last_day_list[2]))


                start_time = times_form.cleaned_data['start_time']
                duration = times_form.cleaned_data['duration']
                stop_time = times_form.cleaned_data['stop_time']

                jstart_time = JDATETIMETOOL.strptime(str(start_time),'%H:%M')
                jstop_time = JDATETIMETOOL.strptime(str(stop_time),'%H:%M')

                today = jdatetime.datetime.now().date()
                stop_2 = JDATETIMETOOL.strptime(str(duration),'%H:%M') +  timedelta(hours=jstart_time.hour, minutes = jstart_time.minute)
                if today > first_day or first_day > last_day or last_data_instance.first_day_2 <= last_day or jstop_time < stop_2 :
                    if not str(stop_time) == '00:00:00':
                        if stop_time > duration:
                            return HttpResponseRedirect(reverse('session:logicalerror'))

                length_2 = last_day - first_day
                length_2 = length_2.days
                if length_2 < 6 :
                    return HttpResponseRedirect(reverse('session:lengtherror'))
                last_data_instance = salon_instance.lastdatas.all()
                if not last_data_instance[0].first_day_2:
                    return HttpResponseRedirect(reverse('session:boundaryerror'))
                if last_day >= last_data_instance[0].first_day_2:
                    return HttpResponseRedirect(reverse('session:boundaryerror'))

                #Checking interferences in sessions we want to create
                existing_sessions = salon_instance.sessions.all()

                for existing_session in existing_sessions:
                    x1 = existing_session.day - first_day
                    x2 = existing_session.day - last_day
                    if int(x1.days) >= 0 and int(x2.days) <= 0 :
                        if str(existing_session.day.weekday()) in selected_days:
                            existing_duration = JDATETIMETOOL.strptime(existing_session.duration,'%H:%M')
                            time_var = existing_duration + timedelta(hours = existing_session.time.hour,
                                                                            minutes = existing_session.time.minute)
                            try:
                                if time_var > ceil :
                                    ceil = time_var
                                    interferenced_session_pk =  existing_session.pk
                            except:
                                ceil = existing_duration +  timedelta(hours = existing_session.time.hour,
                                                                                minutes = existing_session.time.minute)
                                interferenced_session_pk =  existing_session.pk
                            try:
                                if JDATETIMETOOL.strptime(str(existing_session.time),'%H:%M') < floor:
                                    floor = existing_session.time
                                    interferenced_session_pk =  existing_session.pk

                            except:
                                floor = JDATETIMETOOL.strptime(str(existing_session.time),'%H:%M')
                                interferenced_session_pk =  existing_session.pk

                try:
                    if jstart_time < ceil and jstop_time > floor:
                        return HttpResponseRedirect(reverse('session:interferenceerror',
                                                        kwargs={'pk':interferenced_session_pk}))
                except:
                    pass

                #Creating the SessionCategory Instance
                session_category = SessionCategoryModel.objects.create(salon=salon_instance,
                                        range_start_day = first_day, range_end_day = last_day)

                if str(0) in selected_days:
                    session_category.saturdays = True
                    session_category.save()
                if str(1) in selected_days:
                    session_category.sundays = True
                    session_category.save()
                if str(2) in selected_days:
                    session_category.mondays = True
                    session_category.save()
                if str(3) in selected_days:
                    session_category.tuesdays = True
                    session_category.save()
                if str(4) in selected_days:
                    session_category.wednesdays = True
                    session_category.save()
                if str(5) in selected_days:
                    session_category.thursdays = True
                    session_category.save()
                if str(6) in selected_days:
                    session_category.fridays = True
                    session_category.save()


                #creating sessions
                if not duration >= stop_time:
                    x = int(( TotalMinutes(stop_time) - TotalMinutes(start_time) ) / TotalMinutes(duration))
                else:
                    if not str(stop_time) == '00:00:00':
                        x = int(( 1440 + TotalMinutes(stop_time) - TotalMinutes(start_time) ) / TotalMinutes(duration))
                    else:
                        x = int(( 1440 - TotalMinutes(start_time) ) / TotalMinutes(duration))

                day = first_day
                while True:
                    if str(day.weekday()) in selected_days:
                        for i in range(x):
                            total_minutes = TotalMinutes(start_time) + i*TotalMinutes(duration)
                            hours = int(total_minutes/60)
                            minutes = total_minutes - (hours * 60)
                            time = str(hours)+':'+str(minutes)

                            session = SessionModel.objects.create(salon=salon_instance, duration=duration, session_category = session_category,
                                                        day = day, time = time)
                            session.save()
                    day = day + timedelta(days = 1)
                    if day > last_day:
                        break

                return HttpResponseRedirect(reverse('session:workspace',
                                                kwargs={'pk':pk}))
            else:
                print(times_form.errors)
                if times_form.errors:
                    error = True
                days_form_2 = DaysForm_2()
                times_form = TimesForm()
                today = jdatetime.datetime.now().date()
                return render(request,'session/sessioncreate_2.html',
                                      {'times_form':times_form,
                                      'last_data':last_data_instance,
                                      'errors1':error,
                                      'days_form':days_form_2,'today':today,})
        else:
            days_form_2 = DaysForm_2()
            times_form = TimesForm()
            today = jdatetime.datetime.now().date()
            return render(request,'session/sessioncreate_2.html',
                                  {'times_form':times_form,
                                  'last_data':last_data_instance,
                                  'days_form':days_form_2,'today':today,})
    else:
        return HttpResponseRedirect(reverse('login'))


def InterferenceErrorView(request,pk):
    session_instance = get_object_or_404(SessionModel,pk = pk)
    return render(request,'session/interferenceerror.html',{'session':session_instance})


class BoundaryErrorView(TemplateView):
    template_name = 'session/boundaryerror.html'


class NoInputErrorView(TemplateView):
    template_name = 'session/noinputerror.html'


@login_required
@sportclub_required
def SessionCreateView(request, pk):
    salon_instance = get_object_or_404(SalonModel, pk = pk)
    if salon_instance.sportclub.user == request.user:
        try:
            lastdata_instance = get_object_or_404(LastDataModel, salon = salon_instance)
        except:
            lastdata_instance = LastDataModel.objects.create(salon=salon_instance)
        if request.method == 'POST':
            is_closed = request.POST.get('is_closed')
            selected_days = request.POST.getlist('selected_days')
            days_form = DaysForm(data = request.POST )
            times_form = TimesForm(data = request.POST )
            if times_form.is_valid() and days_form.is_valid():

                start_time = times_form.cleaned_data['start_time']
                duration = times_form.cleaned_data['duration']
                stop_time = times_form.cleaned_data['stop_time']


                if not start_time and not duration and not stop_time and not is_closed:
                    return HttpResponseRedirect(reverse('session:noinputerror'))

                if lastdata_instance.last_length:
                    length = lastdata_instance.last_length
                    first_day = lastdata_instance.first_day
                    last_day = lastdata_instance.last_day
                else:
                    if lastdata_instance.first_day_2:
                        first_day = lastdata_instance.first_day_2
                    else:
                        first_day = jdatetime.datetime.now().date()
                    last_day_str = days_form.cleaned_data['last_day']
                    last_day_list = last_day_str.split('-')
                    last_day = jdatetime.date(int(last_day_list[0]),int(last_day_list[1]),int(last_day_list[2]))
                    length = last_day - first_day
                    length = length.days

                if length < 6 :
                    return HttpResponseRedirect(reverse('session:lengtherror'))
                try: # be aware of this try structure before adding any other logical errors
                    jstart_time = JDATETIMETOOL.strptime(str(start_time),'%H:%M')
                    jstop_time = JDATETIMETOOL.strptime(str(stop_time),'%H:%M')
                    stop_2 = JDATETIMETOOL.strptime(str(duration),'%H:%M') +  timedelta(hours=jstart_time.hour, minutes = jstart_time.minute)
                    if first_day > last_day or jstop_time < stop_2:
                        if not str(stop_time) == '00:00:00':
                            if stop_time > duration:
                                return HttpResponseRedirect(reverse('session:logicalerror'))
                except:
                    pass
                #Creating the SessionCategory Instance
                session_category = SessionCategoryModel.objects.create(salon=salon_instance,
                                        range_start_day = first_day, range_end_day = last_day)

                lastdata_instance.first_day = first_day
                lastdata_instance.last_day = last_day
                lastdata_instance.last_length = length
                lastdata_instance.save()

                if str(0) in selected_days:
                    session_category.saturdays = True
                    session_category.save()
                    lastdata_instance.last_saturday = True
                    lastdata_instance.save()
                if str(1) in selected_days:
                    session_category.sundays = True
                    session_category.save()
                    lastdata_instance.last_sunday = True
                    lastdata_instance.save()
                if str(2) in selected_days:
                    session_category.mondays = True
                    session_category.save()
                    lastdata_instance.last_monday = True
                    lastdata_instance.save()
                if str(3) in selected_days:
                    session_category.tuesdays = True
                    session_category.save()
                    lastdata_instance.last_tuesday = True
                    lastdata_instance.save()
                if str(4) in selected_days:
                    session_category.wednesdays = True
                    session_category.save()
                    lastdata_instance.last_wednesday = True
                    lastdata_instance.save()
                if str(5) in selected_days:
                    session_category.thursdays = True
                    session_category.save()
                    lastdata_instance.last_thursday = True
                    lastdata_instance.save()
                if str(6) in selected_days:
                    session_category.fridays = True
                    session_category.save()
                    lastdata_instance.last_friday = True
                    lastdata_instance.save()

                if is_closed == 'closed':
                    session_category.is_closed = True
                    session_category.save()
                    return HttpResponseRedirect(reverse('session:workspace',
                                                    kwargs={'pk':pk}))
                if not duration >= stop_time:
                    x = int(( TotalMinutes(stop_time) - TotalMinutes(start_time) ) / TotalMinutes(duration))
                else:
                    if not str(stop_time) == '00:00:00':
                        x = int(( 1440 + TotalMinutes(stop_time) - TotalMinutes(start_time) ) / TotalMinutes(duration))
                    else:
                        x = int(( 1440 - TotalMinutes(start_time) ) / TotalMinutes(duration))

                day = first_day
                while True:
                    if str(day.weekday()) in selected_days:
                        for i in range(x):
                            total_minutes = TotalMinutes(start_time) + i*TotalMinutes(duration)
                            hours = int(total_minutes/60)
                            minutes = total_minutes - (hours * 60)
                            time = str(hours)+':'+str(minutes)

                            session = SessionModel.objects.create(salon=salon_instance, duration=duration, session_category = session_category,
                                                        day = day, time = time)
                            session.save()
                    day = day + timedelta(days = 1)
                    if day > last_day:
                        break

                return HttpResponseRedirect(reverse('session:workspace',
                                                kwargs={'pk':pk}))
                session_category.range_finish_day = last_day
                session_category.save()
            else:
                print(days_form.errors)
                print(times_form.errors)
                return render(request,'session/createsession.html',{'errors1':days_form.errors,
                                            'errors2':times_form.errors,
                                            'lastdata_instance':lastdata_instance,
                                            'days_form':days_form,
                                            'times_form':times_form,
                                            })

        else:
            days_form = DaysForm()
            times_form = TimesForm()
            return render(request,'session/createsession.html',
                                  {'days_form':days_form,
                                  'times_form':times_form,
                                  'lastdata_instance':lastdata_instance,})
    else:
        return HttpResponseRedirect(reverse('login'))


def LastDataSetView(request, pk):
    salon_instance = get_object_or_404(SalonModel, pk = pk)
    lastdata_instance = get_object_or_404(LastDataModel, salon = salon_instance)
    if salon_instance.sportclub.user == request.user or request.user.is_superuser or request.user.is_masteruser:
        if request.method == 'POST':
            lastdatasetform = LastDataSetForm(data = request.POST )
            if lastdatasetform.is_valid():
                first_day_str = lastdatasetform.cleaned_data['first_day']
                first_day_list = first_day_str.split('-')
                first_day = jdatetime.date(int(first_day_list[0]),int(first_day_list[1]),int(first_day_list[2]))
                lastdata_instance.first_day_2 = first_day
                lastdata_instance.first_day = None
                lastdata_instance.last_day = None
                lastdata_instance.last_length = None
                lastdata_instance.last_saturday = False
                lastdata_instance.last_sunday = False
                lastdata_instance.last_monday = False
                lastdata_instance.last_tuesday = False
                lastdata_instance.last_wednesday = False
                lastdata_instance.last_thursday = False
                lastdata_instance.last_friday = False
                lastdata_instance.save()
                if request.user.is_masteruser:
                    return HttpResponseRedirect(reverse('masteruser:workspace',
                                                    kwargs={'slug':request.user.slug}))
                return HttpResponseRedirect(reverse('session:workspace',
                                                kwargs={'pk':pk}))
            else:
                print(lastdatasetform.errors)
                return HttpResponseRedirect(reverse('session:workspace',
                                                kwargs={'pk':pk}))

        else:
            lastdatasetform = LastDataSetForm()
            return render(request,'session/lastdataset.html',{'form':lastdatasetform})
    else:
        return HttpResponseRedirect(reverse('login'))


class LogicalErrorView(TemplateView):
    template_name = 'session/logicalerror.html'


class IsBookedErrorView(TemplateView):
    template_name = 'session/isbooked.html'


def SessionPublicListView(request):
    today = jdatetime.datetime.now().date()
    now = datetime.datetime.now().time()
    try:
        day_filter = request.session['day_filter']
        time_filter = request.session['time_filter']
        type_filter = request.session['type_filter']
        del request.session['day_filter']
        del request.session['time_filter']
        del request.session['type_filter']
        sessions_1 = SessionModel.objects.filter( salon__is_confirmed = True).filter(is_booked = False).filter(is_ready = True).filter( day = today ).order_by('time').exclude(time__lte=now)
        sessions_2 = SessionModel.objects.filter( salon__is_confirmed = True).filter(is_booked = False).filter(is_ready = True).filter( day__gt = today ).order_by('day','time')
        session_list = sessions_1 | sessions_2
        if time_filter == "1":
            session_list = session_list.filter(time__lte="10:00:00")
        if time_filter == "2":
            session_list = session_list.filter(time__lte="15:00:00").filter(time__gte="10:00:00")
        if time_filter == "3":
            session_list = session_list.filter(time__lte="19:00:00").filter(time__gte="15:00:00")
        if time_filter == "4":
            session_list = session_list.filter(time__gte="19:00:00")

        try:
            session_list = session_list.filter(day=day_filter)
        except:
            pass
        session_filter = SessionFilter(request.GET,queryset = session_list)
        paginator = Paginator(session_filter.qs, 15)
        page = request.GET.get('page')
        sessions = paginator.get_page(page)
        return render(request,'session/publiclist.html',{'sessions':sessions,'filter':session_filter})
    except:
        sessions_1 = SessionModel.objects.filter( salon__is_confirmed = True).filter(is_booked = False).filter(is_ready = True).filter( day = today ).order_by('time').exclude(time__lte=now)
        sessions_2 = SessionModel.objects.filter( salon__is_confirmed = True).filter(is_booked = False).filter(is_ready = True).filter( day__gt = today ).order_by('day','time')
        session_list = sessions_1 | sessions_2
        session_filter = SessionFilter(request.GET,queryset = session_list)
        paginator = Paginator(session_filter.qs, 15)
        page = request.GET.get('page')
        sessions = paginator.get_page(page)
        return render(request,'session/publiclist.html',{'sessions':sessions,'filter':session_filter})


def SessionPublicListForSpecificSalonView(request,pk):
    salon = get_object_or_404(SalonModel,pk = pk)
    today = jdatetime.datetime.now().date()
    now = datetime.datetime.now().time()
    sessions_1 = SessionModel.objects.filter( salon = salon).filter( salon__is_confirmed = True).filter(is_booked = False).filter(is_ready = True).filter( day = today ).order_by('time').exclude(time__lte=now)
    sessions_2 = SessionModel.objects.filter( salon = salon).filter( salon__is_confirmed = True).filter(is_booked = False).filter(is_ready = True).filter( day__gt = today ).order_by('day','time')
    session_list = sessions_1 | sessions_2
    session_filter = SessionFilter(request.GET,queryset = session_list)
    paginator = Paginator(session_filter.qs, 15)
    page = request.GET.get('page')
    sessions = paginator.get_page(page)
    return render(request,'session/publiclistforsalon.html',{'sessions':sessions,'filter':session_filter,'salon':salon,})


def TodaySessionPublicListView(request):
    today = jdatetime.datetime.now().date()
    now = datetime.datetime.now().time()
    session_list = SessionModel.objects.filter( salon__is_confirmed = True).filter(is_booked = False).filter(is_ready = True).filter( day = today ).order_by('time').exclude(time__lte=now)
    session_filter = SessionFilter(request.GET,queryset = session_list)
    paginator = Paginator(session_filter.qs, 15)
    page = request.GET.get('page')
    sessions = paginator.get_page(page)
    return render(request,'session/todaypubliclist.html',{'sessions':sessions,'filter':session_filter})




@login_required
def DayListView(request,pk,str):
    salon = get_object_or_404(SalonModel,pk = pk)
    if request.user == salon.sportclub.user or request.user.is_masteruser:
        sessionlist = get_list_or_404(SessionModel.objects.order_by('day','time'),day = str, salon=salon)
        now = jdatetime.datetime.now().date()
        now_time = jdatetime.datetime.now().time()
        return render(request,'session/daylist.html',{'sessions':sessionlist,'now':now,
        'now_time':now_time,})
    else:
        return HttpResponseRedirect(reverse('login'))



def SessionDetailView(request,pk):
    session = get_object_or_404(SessionModel, pk = pk)
    today = jdatetime.datetime.now().date()
    now_time = datetime.datetime.now().time()
    if session.salon.is_confirmed and session.day >= today and session.is_ready and session.time > now_time:
        price = session.price
        need_to_pay = (((100-session.discount_percentage)/100) * price ) * ((100 - session.salon.company_discount_percentage)/100)
        return render(request,'session/sessiondetail.html',{'session':session,'need_to_pay':need_to_pay})


@method_decorator([login_required, sportclub_required], name='dispatch')
class VirtualBookView(UpdateView):
    model = SessionModel
    fields = ['virtual_booker_name','is_ready',]
    template_name = 'session/virtualbook.html'

    def form_valid(self, form):
        today = jdatetime.datetime.now().date()
        if self.object.day < today:
            return super(VirtualBookView, self).form_invalid(form)
        if form.cleaned_data['is_ready']:
            if not self.object.price:
                 return super(VirtualBookView, self).form_invalid(form)
        if self.object.is_booked:
            return super(VirtualBookView, self).form_invalid(form)
        self.object = form.save()
        self.object.is_ready = False
        self.object.save()
        return super().form_valid(form)

    def get_queryset(self):
        pk = self.kwargs.get(self.pk_url_kwarg)
        obj = get_object_or_404(SessionModel,pk = pk)
        if obj.salon.sportclub.user == self.request.user:
            return self.model._default_manager.all()

    def get_success_url(self):
        pk = self.object.session_category.salon.pk
        return reverse('session:workspace', kwargs={'pk':pk})


def VirtualCancelView(request,pk):
    session = get_object_or_404(SessionModel,pk=pk)
    if session.salon.sportclub.user == request.user:
        session.virtual_booker_name = ''
        session.virtual_booker_name = None
        session.save()
        return HttpResponseRedirect(reverse('session:workspace',kwargs={'pk':session.salon.pk}))
    else:
        return HttpResponseRedirect(reverse('login'))


@login_required
@commonuser_required
def SessionDetailBookingView(request, pk):
    if request.user.is_commonuser:
        session = get_object_or_404(SessionModel, pk=pk)
        salon = session.salon
        today = jdatetime.datetime.now().date()
        now = datetime.datetime.now().time()
        if session.is_ready and session.salon.is_confirmed and session.salon.sportclub.user.is_active and not session.is_booked:
            if session.day > today:
                return render(request,'session/detailforbooking.html',{'session':session,'salon':salon})
            elif session.day == today and session.time >= now:
                return render(request,'session/detailforbooking.html',{'session':session,'salon':salon})
            else:
                return HttpResponseRedirect(reverse('session:notready'))
    else:
        return HttpResponseRedirect(reverse('login'))


def SessionNotReadyErrorView(request):
    return render(request,'session/notready.html')

@login_required
@masteruser_required
def SessionListForSpecificSalonMasterUserView(request,pk):
    salon = get_object_or_404(SalonModel,pk = pk)
    today = jdatetime.datetime.now().date()
    now = datetime.datetime.now().time()
    session_list = SessionModel.objects.filter( salon = salon)
    session_filter = SessionFilter(request.GET,queryset = session_list)
    paginator = Paginator(session_filter.qs, 15)
    page = request.GET.get('page')
    sessions = paginator.get_page(page)
    return render(request,'session/salonlistformasteruser.html',{'sessions':sessions,'filter':session_filter})
