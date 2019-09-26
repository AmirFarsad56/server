
@login_required
@sportclub_required
def noSessionCreateView(request, pk):
    salon_instance = get_object_or_404(SalonModel, pk = pk)
    try:
        lastdata_instance = get_object_or_404(LastDataModel, salon = salon_instance)
    except:
        lastdata_instance = LastDataModel.objects.create(salon=salon_instance)
    if request.method == 'POST':
        days_form = DaysForm(data = request.POST )
        times_form = TimesForm(data = request.POST )
        if times_form.is_valid() and days_form.is_valid():
            if lastdata_instance.last_length:
                length = lastdata_instance.last_length
                first_day = lastdata_instance.first_day
                last_day = lastdata_instance.last_day
                print('333333333333333')
                print(first_day)

            else:
                if lastdata_instance.first_day_2:
                    first_day = lastdata_instance.first_day_2
                    print('222222222222222')
                else:
                    first_day = jdatetime.datetime.now().date()
                    print('1111111111111111')
                print(first_day)
                last_day_str = days_form.cleaned_data['last_day']
                last_day_list = last_day_str.split('-')
                last_day = jdatetime.date(int(last_day_list[0]),int(last_day_list[1]),int(last_day_list[2]))
                length = last_day - first_day
                length = length.days
                print(first_day,';;;;;;;;;;')
            if length < 6 :
                return HttpResponseRedirect(reverse('session:lengtherror'))

            saturdays = days_form.cleaned_data['saturdays']
            sundays = days_form.cleaned_data['sundays']
            mondays = days_form.cleaned_data['mondays']
            tuesdays = days_form.cleaned_data['tuesdays']
            wednesdays = days_form.cleaned_data['wednesdays']
            thursdays = days_form.cleaned_data['thursdays']
            fridays = days_form.cleaned_data['fridays']
            start_time = times_form.cleaned_data['start_time']
            duration = times_form.cleaned_data['duration']
            stop_time = times_form.cleaned_data['stop_time']
            x = int(( TotalMinutes(stop_time) - TotalMinutes(start_time) ) / TotalMinutes(duration))

            #Creating the SessionCategory Instance
            session_category = SessionCategoryModel.objects.create(salon=salon_instance,
                                    range_start_day = first_day, range_end_day = last_day)

            if saturdays:
                session_category.saturdays = True
                session_category.save()
                if lastdata_instance.last_saturday_2:
                    begining_day = lastdata_instance.last_saturday_2 + timedelta(days=1)
                else:
                    begining_day = jdatetime.datetime.now()
                goal_num = len(list(AllSaturdays(length, begining_day)))
                counter_1 = 0
                for days in AllSaturdays(length, begining_day):
                    if days <= last_day :
                        counter_1 += 1
                        for i in range(x):
                            total_minutes = TotalMinutes(start_time) + i*TotalMinutes(duration)
                            hours = int(total_minutes/60)
                            minutes = total_minutes - (hours * 60)
                            time = str(hours)+':'+str(minutes)

                            session = SessionModel.objects.create(salon=salon_instance, duration=duration, session_category = session_category,
                                                        day = str(days), time = time)
                            session.save()
                        if counter_1 == goal_num:
                            first_day = jdatetime.date(first_day.year,first_day.month,first_day.day)
                            last_day = jdatetime.date(last_day.year,last_day.month,last_day.day)
                            lastdata_instance.first_day = first_day
                            lastdata_instance.last_day = last_day
                            lastdata_instance.last_length = length
                            lastdata_instance.last_saturday = days
                            lastdata_instance.save()

            if sundays:
                session_category.sundays = True
                session_category.save()
                if lastdata_instance.last_sunday_2:
                    begining_day = lastdata_instance.last_sunday_2 + timedelta(days=1)
                else:
                    begining_day = jdatetime.datetime.now()
                goal_num = len(list(AllSundays(length, begining_day)))
                counter_1 = 0
                for days in AllSundays(length, begining_day):
                    if days <= last_day :
                        counter_1 += 1
                        for i in range(x):
                            total_minutes = TotalMinutes(start_time) + i*TotalMinutes(duration)
                            hours = int(total_minutes/60)
                            minutes = total_minutes - (hours * 60)
                            time = str(hours)+':'+str(minutes)

                            session = SessionModel.objects.create(salon=salon_instance, duration=duration, session_category = session_category,
                                                        day = str(days), time = time)
                            session.save()
                        if counter_1 == goal_num:
                            first_day = jdatetime.date(first_day.year,first_day.month,first_day.day)
                            last_day = jdatetime.date(last_day.year,last_day.month,last_day.day)
                            lastdata_instance.first_day = first_day
                            lastdata_instance.last_day = last_day
                            lastdata_instance.last_length = length
                            lastdata_instance.last_sunday = days
                            lastdata_instance.save()
            if mondays:
                session_category.mondays = True
                session_category.save()
                if lastdata_instance.last_monday_2:
                    begining_day = lastdata_instance.last_monday_2 + timedelta(days=1)
                else:
                    begining_day = jdatetime.datetime.now()
                goal_num = len(list(AllMondays(length, begining_day)))
                counter_1 = 0
                for days in AllMondays(length, begining_day):
                    if days <= last_day :
                        counter_1 += 1
                        for i in range(x):
                            total_minutes = TotalMinutes(start_time) + i*TotalMinutes(duration)
                            hours = int(total_minutes/60)
                            minutes = total_minutes - (hours * 60)
                            time = str(hours)+':'+str(minutes)

                            session = SessionModel.objects.create(salon=salon_instance, duration=duration, session_category = session_category,
                                                        day = str(days), time = time)
                            session.save()
                        if counter_1 == goal_num:
                            first_day = jdatetime.date(first_day.year,first_day.month,first_day.day)
                            last_day = jdatetime.date(last_day.year,last_day.month,last_day.day)
                            lastdata_instance.first_day = first_day
                            lastdata_instance.last_day = last_day
                            lastdata_instance.last_length = length
                            lastdata_instance.last_monday = days
                            lastdata_instance.save()
            if tuesdays:
                session_category.tuesdays = True
                session_category.save()
                if lastdata_instance.last_tuesday_2:
                    begining_day = lastdata_instance.last_tuesday_2 + timedelta(days=1)
                else:
                    begining_day = jdatetime.datetime.now()
                goal_num = len(list(AllTuesdays(length, begining_day)))
                counter_1 = 0
                for days in AllTuesdays(length, begining_day):
                    if days <= last_day :
                        counter_1 += 1
                        for i in range(x):
                            total_minutes = TotalMinutes(start_time) + i*TotalMinutes(duration)
                            hours = int(total_minutes/60)
                            minutes = total_minutes - (hours * 60)
                            time = str(hours)+':'+str(minutes)

                            session = SessionModel.objects.create(salon=salon_instance, duration=duration, session_category = session_category,
                                                        day = str(days), time = time)
                            session.save()
                        if counter_1 == goal_num:
                            first_day = jdatetime.date(first_day.year,first_day.month,first_day.day)
                            last_day = jdatetime.date(last_day.year,last_day.month,last_day.day)
                            lastdata_instance.first_day = first_day
                            lastdata_instance.last_day = last_day
                            lastdata_instance.last_length = length
                            lastdata_instance.last_tuesday = days
                            lastdata_instance.save()
            if wednesdays:
                session_category.wednesdays = True
                session_category.save()
                if lastdata_instance.last_wednesday_2:
                    begining_day = lastdata_instance.last_wednesday_2 + timedelta(days=1)
                else:
                    begining_day = jdatetime.datetime.now()
                goal_num = len(list(AllWednesdays(length, begining_day)))
                counter_1 = 0
                for days in AllWednesdays(length, begining_day):
                    if days <= last_day :
                        counter_1 += 1
                        for i in range(x):
                            total_minutes = TotalMinutes(start_time) + i*TotalMinutes(duration)
                            hours = int(total_minutes/60)
                            minutes = total_minutes - (hours * 60)
                            time = str(hours)+':'+str(minutes)

                            session = SessionModel.objects.create(salon=salon_instance, duration=duration, session_category = session_category,
                                                        day = str(days), time = time)
                            session.save()
                        if counter_1 == goal_num:
                            first_day = jdatetime.date(first_day.year,first_day.month,first_day.day)
                            last_day = jdatetime.date(last_day.year,last_day.month,last_day.day)
                            lastdata_instance.first_day = first_day
                            lastdata_instance.last_day = last_day
                            lastdata_instance.last_length = length
                            lastdata_instance.last_wednesday = days
                            lastdata_instance.save()
            if thursdays:
                session_category.thursdays = True
                session_category.save()
                if lastdata_instance.last_thursday_2:
                    begining_day = lastdata_instance.last_thursday_2 + timedelta(days=1)
                else:
                    begining_day = jdatetime.datetime.now()
                goal_num = len(list(AllThursdays(length, begining_day)))
                counter_1 = 0
                for days in AllThursdays(length, begining_day):
                    if days <= last_day :
                        counter_1 += 1
                        for i in range(x):
                            total_minutes = TotalMinutes(start_time) + i*TotalMinutes(duration)
                            hours = int(total_minutes/60)
                            minutes = total_minutes - (hours * 60)
                            time = str(hours)+':'+str(minutes)

                            session = SessionModel.objects.create(salon=salon_instance, duration=duration, session_category = session_category,
                                                        day = str(days), time = time)
                            session.save()
                        if counter_1 == goal_num:
                            first_day = jdatetime.date(first_day.year,first_day.month,first_day.day)
                            last_day = jdatetime.date(last_day.year,last_day.month,last_day.day)
                            lastdata_instance.first_day = first_day
                            lastdata_instance.last_day = last_day
                            lastdata_instance.last_length = length
                            lastdata_instance.last_thursday = days
                            lastdata_instance.save()
            if fridays:
                session_category.fridays = True
                session_category.save()
                if lastdata_instance.last_friday_2:
                    begining_day = lastdata_instance.last_friday_2  + timedelta(days=1)
                else:
                    begining_day = jdatetime.datetime.now()
                goal_num = len(list(AllFridays(length, begining_day)))
                counter_1 = 0
                for days in AllFridays(length, begining_day):
                    if days <= last_day :
                        counter_1 += 1
                        for i in range(x):
                            total_minutes = TotalMinutes(start_time) + i*TotalMinutes(duration)
                            hours = int(total_minutes/60)
                            minutes = total_minutes - (hours * 60)
                            time = str(hours)+':'+str(minutes)

                            session = SessionModel.objects.create(salon=salon_instance, duration=duration, session_category = session_category,
                                                        day = str(days), time = time)
                            session.save()
                        if counter_1 == goal_num:
                            first_day = jdatetime.date(first_day.year,first_day.month,first_day.day)
                            last_day = jdatetime.date(last_day.year,last_day.month,last_day.day)
                            lastdata_instance.first_day = first_day
                            lastdata_instance.last_day = last_day
                            lastdata_instance.last_length = length
                            lastdata_instance.last_friday = days
                            lastdata_instance.save()
            return HttpResponseRedirect(reverse('salon:salondetail',
                                            kwargs={'pk':pk}))
            session_category.range_finish_day = last_day
            session_category.save()
        else:
            print(days_form.errors)
            print(times_form.errors)
            return HttpResponseRedirect(reverse('salon:salondetail',
                                            kwargs={'pk':pk}))
    else:
        days_form = DaysForm()
        times_form = TimesForm()
        return render(request,'session/createsession.html',
                              {'days_form':days_form,
                              'times_form':times_form,
                              'lastdata_instance':lastdata_instance,})
