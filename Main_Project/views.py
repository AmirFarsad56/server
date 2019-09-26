from django.views.generic import TemplateView
from django.shortcuts import render
from company.models import SalonAdvertisementModel
from django.shortcuts import get_list_or_404
from session.models import SessionModel
import jdatetime
import datetime

def IndexView(request):
    today = jdatetime.datetime.now().date()
    now = datetime.datetime.now().time()
    salon_advertisement_list = SalonAdvertisementModel.objects.all()
    session_list = [0,]
    i = 0
    for salon in salon_advertisement_list:

        sessions_1 = SessionModel.objects.filter( salon__is_confirmed = True).filter( salon = salon.salon ).filter(is_booked = False).filter(is_ready = True).filter( day = today ).order_by('time').exclude(time__lte=now)
        sessions_2 = SessionModel.objects.filter( salon__is_confirmed = True).filter( salon = salon.salon ).filter(is_booked = False).filter(is_ready = True).filter( day__gt = today ).order_by('day','time')
        sessions = sessions_1 | sessions_2
        for counter in range(3):
            try:
                session_list.append(sessions[counter])
            except:
                pass

    return render(request,'index.html',{'salons':salon_advertisement_list,'sessions':session_list})
