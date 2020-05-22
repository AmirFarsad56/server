from django.shortcuts import render, redirect
from django.views.generic import DetailView, ListView, TemplateView
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
from django.utils.text import slugify
from django.shortcuts import get_object_or_404, get_list_or_404
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.utils import timezone
from django.core.paginator import Paginator
import jdatetime
from django.core.serializers import serialize
from django.conf import settings

#SMS send
from kavenegar import KavenegarAPI

#handmade classes
from accounts.models import UserModel
from sportclub.filters import SportClubFilter
from sportclub.forms import SportClubForm, TermsAndConditionsForm
from accounts.forms import UserForm, UserUpdateForm
from sportclub.models import SportClubModel
from accounts.models import UserModel
from salon.models import SalonModel
from sportclub.decorators import sportclub_required
from accounts.decorators import superuser_required
from masteruser.decorators import masteruser_required
from sportclub.forms import MessageForm, EmailForm, BankInfoForm, SportClubUpdateForm

#recaptcha
import json
import urllib
from django.conf import settings
from django.contrib import messages

@masteruser_required
def SportClubSignupView(request):
    registered = False

    if request.method == 'POST':

        user_form = UserForm(data = request.POST)
        sportclub_form = SportClubForm(data = request.POST)
        region = request.POST.get('region')

        if user_form.is_valid() and sportclub_form.is_valid():
                     '''
                recaptcha_response = request.POST.get('g-recaptcha-response')
                url = 'https://www.google.com/recaptcha/api/siteverify'
                values = {
                    'secret': settings.GOOGLE_RECAPTCHA_SECRET_KEY,
                    'response': recaptcha_response
                }
                data = urllib.parse.urlencode(values).encode()
                req =  urllib.request.Request(url, data=data)
                response = urllib.request.urlopen(req)
                result = json.loads(response.read().decode())
                if result['success']:
                     '''
                     messages.success(request, 'ثبت نام با موفقیت انجام شد')
                     user = user_form.save(commit = False)#changed this if sth wrong happen ..
                     user.is_sportclub = True
                     user.save()
                     sportclub = sportclub_form.save(commit=False)
                     sportclub.user = user
                     sportclub.region = region
                     sportclub.serial_number = sportclub.pk + 1000
                     sportclub.phone_number = '0' + user.username
                     print(sportclub.phone_number)
                     if 'picture' in request.FILES:
                        sportclub.picture = request.FILES['picture']

                     sportclub.save()
                     registered = True
                     masteruser_instance = get_object_or_404(UserModel, slug = request.user.slug)
                     masteruser_instance_logs = masteruser_instance.user_logs
                     now = jdatetime.datetime.now()
                     dtime = str(now.year)+'-'+str(now.month)+'-'+ str(now.day)+'  '+str(now.hour)+':'+str(now.minute)+':'+str(now.second)
                     new_log = '''{previous_logs}\n
 On {date_time}:\n
 Created SportClub: {sportclub}
 -------------------------------------------------------
                     '''.format(previous_logs = masteruser_instance_logs,
                                date_time = dtime,
                                 sportclub = str(user.username),)
                     masteruser_instance.user_logs = new_log
                     masteruser_instance.save()
                #else:
                #     messages.error(request, 'فیلد من ربات نیستم را به درستی کامل کنید')

        else:
            # One of the forms was invalid if this else gets called.
            #redirect to another page or anything else
            print(user_form.errors,sportclub_form.errors)


    else:
        user_form = UserForm()
        sportclub_form = SportClubForm()

    return render(request,'sportclub/sportclubsignup.html',
                          {'user_form':user_form,
                           'sportclub_form':sportclub_form,
                           'registered':registered})


@sportclub_required
@login_required
def SportClubProfileView(request, slug):
    user = request.user
    SportClubDetail = get_object_or_404(SportClubModel, user = user)
    return render(request,'sportclub/profile.html',
                    {'sportclub_detail':SportClubDetail})


@sportclub_required
@login_required
def SportClubWorkSpaceView(request, slug):
    user_instance = get_object_or_404(UserModel,slug = slug)
    if user_instance == request.user:
        SportClubDetail = get_object_or_404(SportClubModel, user = user_instance)
        return render(request,'sportclub/workspace.html',
                        {'sportclub_detail':SportClubDetail})
    else:
        return HttpResponseRedirect(reverse('login'))


@login_required
@masteruser_required
def SportClubListView(request):
    sportclub_list = SportClubModel.objects.all()
    sportclub_filter = SportClubFilter(request.GET,queryset = sportclub_list)
    paginator = Paginator(sportclub_filter.qs, 20)
    page = request.GET.get('page')
    sportclubs = paginator.get_page(page)
    return render(request,'sportclub/sportclublist.html',{'sportclubs':sportclubs,'filter':sportclub_filter})


@login_required
@superuser_required
def SportClubListViewSuperUser(request):
    sportclub_list = SportClubModel.objects.all()
    sportclub_filter = SportClubFilter(request.GET,queryset = sportclub_list)
    paginator = Paginator(sportclub_filter.qs, 20)
    page = request.GET.get('page')
    sportclubs = paginator.get_page(page)
    return render(request,'sportclub/sportclublistsuperuser.html',{'sportclubs':sportclubs,'filter':sportclub_filter})


def SportClubDetailView(request,slug):
    user_instance = get_object_or_404(UserModel, slug = slug)
    sportclub_instance = get_object_or_404(SportClubModel, user = user_instance)

    try:
        salon_instances = get_list_or_404(SalonModel, sportclub = sportclub_instance)
        return render(request,'sportclub/sportclubdetail.html',
                      {'sportclub_detail':sportclub_instance,
                       'salons':salon_instances})
    except:
        return render(request,'sportclub/sportclubdetail.html',
                      {'sportclub_detail':sportclub_instance})


@login_required
@masteruser_required
def UnBanModalView(request,slug):
    if request.user.is_masteruser:
        user_instance = get_object_or_404(UserModel, slug = slug)
        sportclub_instance = get_object_or_404(SportClubModel, user = user_instance)
        return render(request,'sportclub/unbanmodal.html',
                      {'sportclub':sportclub_instance})
    else:
        return HttpResponseRedirect(reverse('login'))


@login_required
@masteruser_required
def UnBanModalView_2(request,slug):
    if request.user.is_masteruser:
        user_instance = get_object_or_404(UserModel, slug = slug)
        sportclub_instance = get_object_or_404(SportClubModel, user = user_instance)

        return render(request,'sportclub/unbanmodal2.html',
                      {'sportclub':sportclub_instance})
    else:
        return HttpResponseRedirect(reverse('login'))


@login_required
@masteruser_required
def UnBanModalView_3(request,slug):
    if request.user.is_masteruser:
        user_instance = get_object_or_404(UserModel, slug = slug)
        sportclub_instance = get_object_or_404(SportClubModel, user = user_instance)
        return render(request,'sportclub/unbanmodal3.html',
                      {'sportclub':sportclub_instance})
    else:
        return HttpResponseRedirect(reverse('login'))


@login_required
@masteruser_required
def BanModalView(request,slug):
    if request.user.is_masteruser:
        user_instance = get_object_or_404(UserModel, slug = slug)
        sportclub_instance = get_object_or_404(SportClubModel, user = user_instance)
        return render(request,'sportclub/banmodal.html',
                      {'sportclub':sportclub_instance})
    else:
        return HttpResponseRedirect(reverse('login'))


@login_required
@masteruser_required
def BanModalView_2(request,slug):
    if request.user.is_masteruser:
        user_instance = get_object_or_404(UserModel, slug = slug)
        sportclub_instance = get_object_or_404(SportClubModel, user = user_instance)
        return render(request,'sportclub/banmodal2.html',
                      {'sportclub':sportclub_instance})
    else:
        return HttpResponseRedirect(reverse('login'))


@login_required
@masteruser_required
def BanModalView_3(request,slug):
    if request.user.is_masteruser:
        user_instance = get_object_or_404(UserModel, slug = slug)
        sportclub_instance = get_object_or_404(SportClubModel, user = user_instance)
        return render(request,'sportclub/banmodal3.html',
                      {'sportclub':sportclub_instance})
    else:
        return HttpResponseRedirect(reverse('login'))



@login_required
@superuser_required
def SportClubDetailViewSuperUser(request,slug):
    if request.user.is_superuser:
        user_instance = get_object_or_404(UserModel, slug = slug)
        sportclub_instance = get_object_or_404(SportClubModel, user = user_instance)

        try:
            salon_instances = get_list_or_404(SalonModel, sportclub = sportclub_instance)
            return render(request,'sportclub/sportclubdetailsuperuser.html',
                          {'sportclub_detail':sportclub_instance,
                           'salons':salon_instances})
        except:
            return render(request,'sportclub/sportclubdetailsuperuser.html',
                          {'sportclub_detail':sportclub_instance})
    else:
        return HttpResponseRedirect(reverse('login'))


@login_required
@masteruser_required
def BannedSportClubExceptionView(request,slug):
    if request.user.is_masteruser:
        user_instance = get_object_or_404(UserModel, slug = slug)
        sportclub_instance = get_object_or_404(SportClubModel, user = user_instance)
        salon_instances = get_list_or_404(SalonModel, sportclub = sportclub_instance)
        return render(request,'sportclub/bannedsportclubexception.html',
                      {'sportclub_detail':sportclub_instance,
                       'salons':salon_instances})
    else:
        return HttpResponseRedirect(reverse('login'))


@login_required
@masteruser_required
def SportClubBanView(request,slug):
    if request.user.is_masteruser:
        user_instance = get_object_or_404(UserModel, slug = slug)

        sportclub_instance = get_object_or_404(SportClubModel, user = user_instance)

        try:
            salon_instances = get_list_or_404(SalonModel, sportclub = sportclub_instance)
            for salon_instance in salon_instances:
                salon_instance.is_confirmed = False
                salon_instance.save()
        except:
            pass
        user_instance.is_active = False
        user_instance.save()
        masteruser_instance = get_object_or_404(UserModel, slug = request.user.slug)
        masteruser_instance_logs = masteruser_instance.user_logs
        now = jdatetime.datetime.now()
        dtime = str(now.year)+'-'+str(now.month)+'-'+ str(now.day)+'  '+str(now.hour)+':'+str(now.minute)+':'+str(now.second)
        new_log = '''{previous_logs}\n
On {date_time}:\n
Banned Sportclub: {user}
-------------------------------------------------------
        '''.format(previous_logs = masteruser_instance_logs,
                   date_time = dtime,
                    user = str(user_instance.username),)
        masteruser_instance.user_logs = new_log
        masteruser_instance.save()
        return HttpResponseRedirect(reverse("sportclub:list"))
    else:
        return HttpResponseRedirect(reverse('login'))


@login_required
@masteruser_required
def SportClubBanView_2(request,slug):
    if request.user.is_masteruser:
        user_instance = get_object_or_404(UserModel, slug = slug)

        sportclub_instance = get_object_or_404(SportClubModel, user = user_instance)

        try:
            salon_instances = get_list_or_404(SalonModel, sportclub = sportclub_instance)
            for salon_instance in salon_instances:
                salon_instance.is_confirmed = False
                salon_instance.save()
        except:
            pass
        user_instance.is_active = False
        user_instance.save()
        masteruser_instance = get_object_or_404(UserModel, slug = request.user.slug)
        masteruser_instance_logs = masteruser_instance.user_logs
        now = jdatetime.datetime.now()
        dtime = str(now.year)+'-'+str(now.month)+'-'+ str(now.day)+'  '+str(now.hour)+':'+str(now.minute)+':'+str(now.second)
        new_log = '''{previous_logs}\n
On {date_time}:\n
Banned Sportclub: {user}
-------------------------------------------------------
        '''.format(previous_logs = masteruser_instance_logs,
                   date_time = dtime,
                    user = str(user_instance.username),)
        masteruser_instance.user_logs = new_log
        masteruser_instance.save()
        return HttpResponseRedirect(reverse("salon:confirmedsalonlist"))
    else:
        return HttpResponseRedirect(reverse('login'))


@login_required
@masteruser_required
def SportClubBanView_3(request,slug):
    if request.user.is_masteruser:
        user_instance = get_object_or_404(UserModel, slug = slug)

        sportclub_instance = get_object_or_404(SportClubModel, user = user_instance)

        try:
            salon_instances = get_list_or_404(SalonModel, sportclub = sportclub_instance)
            for salon_instance in salon_instances:
                salon_instance.is_confirmed = False
                salon_instance.save()
        except:
            pass
        user_instance.is_active = False
        user_instance.save()
        masteruser_instance = get_object_or_404(UserModel, slug = request.user.slug)
        masteruser_instance_logs = masteruser_instance.user_logs
        now = jdatetime.datetime.now()
        dtime = str(now.year)+'-'+str(now.month)+'-'+ str(now.day)+'  '+str(now.hour)+':'+str(now.minute)+':'+str(now.second)
        new_log = '''{previous_logs}\n
On {date_time}:\n
Banned Sportclub: {user}
-------------------------------------------------------
        '''.format(previous_logs = masteruser_instance_logs,
                   date_time = dtime,
                    user = str(user_instance.username),)
        masteruser_instance.user_logs = new_log
        masteruser_instance.save()
        return HttpResponseRedirect(reverse("salon:unconfirmedsalonlist"))
    else:
        return HttpResponseRedirect(reverse('login'))


@login_required
@masteruser_required
def SportClubUnBanView(request,slug):
    if request.user.is_masteruser:
        user_instance = get_object_or_404(UserModel, slug = slug)
        user_instance.is_active = True
        user_instance.save()
        masteruser_instance = get_object_or_404(UserModel, slug = request.user.slug)
        masteruser_instance_logs = masteruser_instance.user_logs
        now = jdatetime.datetime.now()
        dtime = str(now.year)+'-'+str(now.month)+'-'+ str(now.day)+'  '+str(now.hour)+':'+str(now.minute)+':'+str(now.second)
        new_log = '''{previous_logs}\n
On {date_time}:\n
UnBanned Sportclub: {user}
-------------------------------------------------------
        '''.format(previous_logs = masteruser_instance_logs,
                   date_time = dtime,
                    user = str(user_instance.username),)
        masteruser_instance.user_logs = new_log
        masteruser_instance.save()
        return HttpResponseRedirect(reverse("sportclub:bannedlist"))
    else:
        return HttpResponseRedirect(reverse('login'))



@login_required
@masteruser_required
def SportClubUnBanView_2(request,slug):
    if request.user.is_masteruser:
        user_instance = get_object_or_404(UserModel, slug = slug)
        user_instance.is_active = True
        user_instance.save()
        masteruser_instance = get_object_or_404(UserModel, slug = request.user.slug)
        masteruser_instance_logs = masteruser_instance.user_logs
        now = jdatetime.datetime.now()
        dtime = str(now.year)+'-'+str(now.month)+'-'+ str(now.day)+'  '+str(now.hour)+':'+str(now.minute)+':'+str(now.second)
        new_log = '''{previous_logs}\n
On {date_time}:\n
UnBanned Sportclub: {user}
-------------------------------------------------------
        '''.format(previous_logs = masteruser_instance_logs,
                   date_time = dtime,
                    user = str(user_instance.username),)
        masteruser_instance.user_logs = new_log
        masteruser_instance.save()
        return HttpResponseRedirect(reverse("salon:confirmedsalonlist"))
    else:
        return HttpResponseRedirect(reverse('login'))


@login_required
@masteruser_required
def SportClubUnBanView_3(request,slug):
    if request.user.is_masteruser:
        user_instance = get_object_or_404(UserModel, slug = slug)
        user_instance.is_active = True
        user_instance.save()
        masteruser_instance = get_object_or_404(UserModel, slug = request.user.slug)
        masteruser_instance_logs = masteruser_instance.user_logs
        now = jdatetime.datetime.now()
        dtime = str(now.year)+'-'+str(now.month)+'-'+ str(now.day)+'  '+str(now.hour)+':'+str(now.minute)+':'+str(now.second)
        new_log = '''{previous_logs}\n
On {date_time}:\n
UnBanned Sportclub: {user}
-------------------------------------------------------
        '''.format(previous_logs = masteruser_instance_logs,
                   date_time = dtime,
                    user = str(user_instance.username),)
        masteruser_instance.user_logs = new_log
        masteruser_instance.save()
        return HttpResponseRedirect(reverse("salon:unconfirmedsalonlist"))
    else:
        return HttpResponseRedirect(reverse('login'))



@login_required
@superuser_required
def SportClubDeleteView(request,slug):
    if request.user.is_masteruser:
        user_instance = get_object_or_404(UserModel, slug = slug)
        sportclub_instance = get_object_or_404(SportClubModel, user = user_instance)
        sportclub_instance.delete()
        masteruser_instance = get_object_or_404(UserModel, slug = request.user.slug)
        masteruser_instance_logs = masteruser_instance.user_logs
        now = jdatetime.datetime.now()
        dtime = str(now.year)+'-'+str(now.month)+'-'+ str(now.day)+'  '+str(now.hour)+':'+str(now.minute)+':'+str(now.second)
        new_log = '''{previous_logs}\n
On {date_time}:\n
Deleted Sportclub: {user}
-------------------------------------------------------
        '''.format(previous_logs = masteruser_instance_logs,
                   date_time = dtime,
                   user = str(user_instance.username),)
        masteruser_instance.user_logs = new_log
        masteruser_instance.save()
        user_instance.delete()

        return HttpResponseRedirect(reverse('sportclub:bannedlist'))
    else:
        return HttpResponseRedirect(reverse('login'))


@login_required
@masteruser_required
def BannedSportClubListView(request):
    sportclub_list = SportClubModel.objects.all()
    sportclub_filter = SportClubFilter(request.GET,queryset = sportclub_list)
    paginator = Paginator(sportclub_filter.qs, 20)
    page = request.GET.get('page')
    sportclubs = paginator.get_page(page)
    return render(request,'sportclub/bannedsportclublist.html',{'sportclubs':sportclubs,'filter':sportclub_filter})


@login_required
@masteruser_required
def MesssageSendingView(request,slug):
    api = KavenegarAPI(settings.KAVENEGAR_API_KEY)
    if request.user.is_masteruser:
        user_instance = get_object_or_404(UserModel, slug = slug)
        sportclub_instance = get_object_or_404(SportClubModel, user = user_instance)
        if request.method == 'POST':
            message_form = MessageForm(data = request.POST)
            if message_form.is_valid():
                message_text = message_form.cleaned_data.get('text')
                params = {
                'sender': settings.KAVENEGAR_PHONE_NUMBER,
                'receptor': sportclub_instance.phone_number,
                'message' : message_text
                }
                response = api.sms_send(params)

                masteruser_instance = get_object_or_404(UserModel, slug = request.user.slug)
                masteruser_instance_logs = masteruser_instance.user_logs
                now = jdatetime.datetime.now()
                dtime = str(now.year)+'-'+str(now.month)+'-'+ str(now.day)+'  '+str(now.hour)+':'+str(now.minute)+':'+str(now.second)
                new_log = '''{previous_logs}\n
On {date_time}:\n
Sent a Message to: {user} (Sport Club)\n
Message:\n
{message}
-------------------------------------------------------
                '''.format(previous_logs = masteruser_instance_logs,
                           date_time = dtime,
                            user = str(sportclub_instance.user.username),
                            message = str(message_text),)
                masteruser_instance.user_logs = new_log
                masteruser_instance.save()
                return HttpResponseRedirect(reverse('masteruser:workspace',
                                            kwargs={'slug':request.user.slug}))
        else:
            message_form = MessageForm()

            return render(request,'sportclub/messageform.html',
                                  {'form':message_form,})


@login_required
@masteruser_required
def EmailSendingView(request,slug):
    if request.user.is_masteruser:
        user_instance = get_object_or_404(UserModel, slug = slug)
        sportclub_instance = get_object_or_404(SportClubModel, user = user_instance)
        if request.method == 'POST':
            email_form = EmailForm(data = request.POST)
            if email_form.is_valid():
                email_subject = email_form.cleaned_data.get('subject')
                email_text = email_form.cleaned_data.get('text')
                send_mail(
                email_subject,
                email_text,
                'info@varzesh-kon.ir',
                [user_instance.email,],
                fail_silently=False,
                )
                masteruser_instance = get_object_or_404(UserModel, slug = request.user.slug)
                masteruser_instance_logs = masteruser_instance.user_logs
                now = jdatetime.datetime.now()
                dtime = str(now.year)+'-'+str(now.month)+'-'+ str(now.day)+'  '+str(now.hour)+':'+str(now.minute)+':'+str(now.second)
                new_log = '''{previous_logs}\n
On {date_time}:\n
Sent an Email to: {user} (Sport Club)\n
Email Subject:
{subject}\n
Email Text:\n
{text}
-------------------------------------------------------
                '''.format(previous_logs = masteruser_instance_logs,
                           date_time = dtime,
                            user = str(sportclub_instance.user.username),
                            subject = str(email_subject),
                            text = str(email_text),)
                masteruser_instance.user_logs = new_log
                masteruser_instance.save()
                return HttpResponseRedirect(reverse('masteruser:workspace',
                                            kwargs={'slug':request.user.slug}))
        else:
            email_form = EmailForm()

            return render(request,'sportclub/emailform.html',
                                  {'form':email_form,})


@login_required
@sportclub_required
def BankInfoChangeView(request,slug):
    sportclub_user = get_object_or_404(UserModel,slug = slug)
    sportclub = get_object_or_404(SportClubModel,user = sportclub_user)
    bank_info_form = BankInfoForm(request.POST or None, instance = sportclub)
    if bank_info_form.is_valid():
        bank_info_form.save()
        return HttpResponseRedirect(reverse('sportclub:profile',
                                    kwargs={'slug':sportclub_user.slug}))
    return render(request,'sportclub/bankinfochange.html',
                          {'bankinfoform':bank_info_form,})


@login_required
@sportclub_required
def SportClubUpdateView(request,slug):
    sportclub_user = get_object_or_404(UserModel,slug = slug)
    user_update_form = UserUpdateForm(request.POST or None, instance = sportclub_user)
    region = request.POST.get('region')
    sportclub = get_object_or_404(SportClubModel,user = sportclub_user)
    sportclub_update_form = SportClubUpdateForm(request.POST or None, instance = sportclub)
    if user_update_form.is_valid() and sportclub_update_form.is_valid():
        user_update_form.save()
        sportclub_update_form.save()
        if region:
            sportclub.region = region
        if 'picture' in request.FILES:
           sportclub.picture = request.FILES['picture']
           sportclub.save()
        sportclub.save()
        return HttpResponseRedirect(reverse('sportclub:profile',
                                    kwargs={'slug':sportclub_user.slug}))
    return render(request,'sportclub/sportclubupdate.html',
                          {'sportclubform':sportclub_update_form,
                           'userform':user_update_form,})


@login_required
@sportclub_required
def TermsAndConditionsView(request,slug):
    sportclub_user = get_object_or_404(UserModel,slug = slug)
    sportclub = get_object_or_404(SportClubModel,user = sportclub_user)
    terms_and_conditions_form = TermsAndConditionsForm(request.POST or None, instance = sportclub)
    if terms_and_conditions_form.is_valid():
        terms_and_conditions_form.save()
        return HttpResponseRedirect(reverse('sportclub:profile',
                                    kwargs={'slug':sportclub_user.slug}))
    return render(request,'sportclub/termsandconditions.html',
                          {'form':terms_and_conditions_form,})


def MapDataSetView(request):
    try:
        query = get_list_or_404(SportClubModel)
    except:
        pass
    try:
        points = serialize('geojson',query)
    except:
        points = False
    return HttpResponse(points, content_type = 'json')



def MapView(request):
    return render(request,'sportclub/map.html')


class NoAccountDetailErrorView(TemplateView):
    template_name = 'sportclub/noaccountdetailerror.html'



def SportClubPublicListView(request):
    sportclub_list = SportClubModel.objects.filter(user__is_active = True)
    sportclub_filter = SportClubFilter(request.GET,queryset = sportclub_list)
    paginator = Paginator(sportclub_filter.qs, 10)
    page = request.GET.get('page')
    sportclubs = paginator.get_page(page)
    return render(request,'sportclub/publiclist.html',{'sportclubs':sportclubs,'filter':sportclub_filter})
