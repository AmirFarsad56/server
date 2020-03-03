info@varzesh-kon.irfrom django.shortcuts import render, redirect
from django.views.generic import ListView, DetailView
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.utils.text import slugify
from django.shortcuts import get_object_or_404
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
import jdatetime
import datetime
import random
from django.conf import settings
from django.utils import timezone

#SMS send
from django.utils import timezone
from kavenegar import KavenegarAPI

#handmade classes
from booking.models import BookingModel, ContractModel
from session.models import SessionModel
from commonuser.forms import CommonUserForm, CommonUserUpdateForm
from accounts.forms import UserForm, UserUpdateForm
from commonuser.models import CommonUserModel
from accounts.models import UserModel
from masteruser.decorators import masteruser_required
from commonuser.decorators import commonuser_required
from commonuser.forms import MessageForm, EmailForm, ConfirmationForm

#recaptcha
import json
import urllib
from django.conf import settings
from django.contrib import messages

#message send
from kavenegar import KavenegarAPI


def CommonUserSignupView(request):
    api = KavenegarAPI(settings.KAVENEGAR_API_KEY)
    try:
        last_retry_str = request.session['last_retry']
        last_retry = datetime.datetime.strptime(last_retry_str,"%Y-%m-%d %H:%M:%S")
    except:
        last_retry = datetime.datetime.now()
    now = datetime.datetime.now()
    if now >= last_retry:
        if request.method == 'POST':

            user_form = UserForm(data = request.POST)
            commonuser_form = CommonUserForm(data = request.POST)

            if user_form.is_valid() and commonuser_form.is_valid():
                 phone_number = commonuser_form.cleaned_data.get('phone_number')


                 user = user_form.save(commit=False)
                 user.is_commonuser = True
                 user.is_active = False
                 user.save()

                 request.session['user_slug'] =  user.slug
                 commonuser = commonuser_form.save(commit=False)
                 commonuser.user = user
                 commonuser.save()
                 #### generating code
                 var = '1234567890'
                 random_code=''
                 for i in range(5):
                     c = random.choice(var)
                     random_code += c
                 ######
                 code = random_code
                 ######### send code to commonuser
                 params = {
                 'sender': settings.KAVENEGAR_PHONE_NUMBER,
                 'receptor': phone_number,
                 'message' : 'سامانه ورزش کن \n' +'کد فعالسازی شما' +  ' :' + code
                 }
                 try:
                     response = api.sms_send(params)
                     request.session['code'] =  code
                     request.session['phone_number'] =  phone_number
                     now = datetime.datetime.now() + datetime.timedelta(minutes=1)
                     str_now = str(now.year)+'-'+str(now.month)+'-'+str(now.day)+' '+str(now.hour)+':'+str(now.minute)+':'+str(now.second)
                     request.session['last_retry'] = str_now

                 #################################
                 except:
                     return HttpResponseRedirect(reverse('accounts:wrongphonenumber'))

                 return HttpResponseRedirect(reverse('commonuser:confirmation'))
            else:
                # One of the forms was invalid if this else gets called.
                #redirect to another page or anything else
                print(user_form.errors,commonuser_form.errors)


        else:
            user_form = UserForm()
            commonuser_form = CommonUserForm()

        return render(request,'commonuser/commonusersignup.html',
                              {'user_form':user_form,
                               'commonuser_form':commonuser_form})
    else:
        return HttpResponseRedirect(reverse('commonuser:twominwait'))


def UserConfirmView(request):

    user_slug = request.session['user_slug']
    code = request.session['code']
    user_instance = get_object_or_404(UserModel,slug = user_slug)
    if request.method == 'POST':

        confirmation_form = ConfirmationForm(data = request.POST)

        if confirmation_form.is_valid():
            confirmation_code = confirmation_form.cleaned_data.get('code')
            print(confirmation_code,code)
            if confirmation_code == code:
                user_instance.is_active = True
                user_instance.save()
                return HttpResponseRedirect(reverse('login'))
        else:
            print(confirmation_form.errors,)


    else:
        confirmation_form = ConfirmationForm()
        phone_number = request.session['phone_number']
    return render(request,'commonuser/confirmation.html',
                          {'confirmation_form':confirmation_form,'phone_number':phone_number})
#    except:
#        return HttpResponseRedirect(reverse('commonuser:signup'))


def TwoMinWaitView(request):
    return render(request,'commonuser/twominwait.html')


@login_required
def CommonUserProfileView(request,slug):
    user_instance = get_object_or_404(UserModel,slug = slug)
    commonuser_instance = get_object_or_404(CommonUserModel, user = user_instance)
    if request.user == user_instance:
        return render(request,'commonuser/commonuserprofile.html',
                     {'commonuser_detail':commonuser_instance})


@method_decorator([login_required, masteruser_required], name='dispatch')
class CommonUserListView(ListView):
    model = CommonUserModel
    context_object_name = 'commonusers'
    template_name = 'commonuser/commonuserlist.html'


@login_required
@masteruser_required
def CommonUserBanView(request,slug):
    if request.user.is_masteruser:
        user_instance = get_object_or_404(UserModel, slug = slug)
        user_instance.is_active = False
        user_instance.save()
        masteruser_instance = get_object_or_404(UserModel, slug = request.user.slug)
        masteruser_instance_logs = masteruser_instance.user_logs
        now = jdatetime.datetime.now()
        dtime = str(now.year)+'-'+str(now.month)+'-'+ str(now.day)+'  '+str(now.hour)+':'+str(now.minute)+':'+str(now.second)
        new_log = '''{previous_logs}\n
On {date_time}:\n
Banned CommonUser: {user}
-------------------------------------------------------
        '''.format(previous_logs = masteruser_instance_logs,
                   date_time = dtime,
                    user = str(user_instance.username),)
        masteruser_instance.user_logs = new_log
        masteruser_instance.save()
        return HttpResponseRedirect(reverse("commonuser:list"))
    else:
        return HttpResponseRedirect(reverse('login'))


@login_required
@masteruser_required
def CommonUserUnBanView(request,slug):
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
UnBanned CommonUser: {user}
-------------------------------------------------------
        '''.format(previous_logs = masteruser_instance_logs,
                   date_time = dtime,
                    user = str(user_instance.username),)
        masteruser_instance.user_logs = new_log
        masteruser_instance.save()
        return HttpResponseRedirect(reverse("commonuser:bannedlist"))
    else:
        return HttpResponseRedirect(reverse('login'))


@login_required
@masteruser_required
def CommonUserDeleteView(request,slug):
    if request.user.is_masteruser:
        user_instance = get_object_or_404(UserModel, slug = slug)
        commonuser_instance = get_object_or_404(CommonUserModel, user = user_instance)
        commonuser_instance.delete()
        masteruser_instance = get_object_or_404(UserModel, slug = request.user.slug)
        masteruser_instance_logs = masteruser_instance.user_logs
        now = jdatetime.datetime.now()
        dtime = str(now.year)+'-'+str(now.month)+'-'+ str(now.day)+'  '+str(now.hour)+':'+str(now.minute)+':'+str(now.second)
        new_log = '''{previous_logs}\n
On {date_time}:\n
Deleted CommonUser: {user}
-------------------------------------------------------
        '''.format(previous_logs = masteruser_instance_logs,
                   date_time = dtime,
                    user = str(user_instance.username),)
        masteruser_instance.user_logs = new_log
        masteruser_instance.save()
        user_instance.delete()
        return HttpResponseRedirect(reverse('commonuser:bannedlist'))
    else:
        return HttpResponseRedirect(reverse('login'))


@method_decorator([login_required, masteruser_required], name='dispatch')
class BannedCommonUserListView(ListView):
    model = CommonUserModel
    context_object_name = 'commonusers'
    template_name = 'commonuser/bannedcommonuserlist.html'



@login_required
@masteruser_required
def MesssageSendingView(request,slug):
    api = KavenegarAPI(settings.KAVENEGAR_API_KEY)
    if request.user.is_masteruser:
        user_instance = get_object_or_404(UserModel, slug = slug)
        commonuser_instance = get_object_or_404(CommonUserModel, user = user_instance)
        if request.method == 'POST':
            message_form = MessageForm(data = request.POST)
            if message_form.is_valid():
                message_text = message_form.cleaned_data.get('text')
                params = {
                'sender': settings.KAVENEGAR_PHONE_NUMBER,
                'receptor': commonuser_instance.phone_number,
                'message' : message_text
                }
                response = api.sms_send(params)

                masteruser_instance = get_object_or_404(UserModel, slug = request.user.slug)
                masteruser_instance_logs = masteruser_instance.user_logs
                now = jdatetime.datetime.now()
                dtime = str(now.year)+'-'+str(now.month)+'-'+ str(now.day)+'  '+str(now.hour)+':'+str(now.minute)+':'+str(now.second)
                new_log = '''{previous_logs}\n
On {date_time}:\n
Sent a message to: {user} (Common User)\n
Message:\n
{message}
-------------------------------------------------------
                '''.format(previous_logs = masteruser_instance_logs,
                           date_time = dtime,
                            user = str(commonuser_instance.user.username),
                            message = str(message_text),)

                masteruser_instance.user_logs = new_log
                masteruser_instance.save()
                return HttpResponseRedirect(reverse('commonuser:list'))
        else:
            message_form = MessageForm()

            return render(request,'commonuser/messageform.html',
                                  {'form':message_form,})


@login_required
@masteruser_required
def EmailSendingView(request,slug):
    if request.user.is_masteruser:
        user_instance = get_object_or_404(UserModel, slug = slug)
        commonuser_instance = get_object_or_404(CommonUserModel, user = user_instance)
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
Sent an Email to: {user} (Common User)\n
Email Subject:
{subject}\n
Email Text:\n
{text}
-------------------------------------------------------
                '''.format(previous_logs = masteruser_instance_logs,
                           date_time = dtime,
                            user = str(commonuser_instance.user.username),
                            subject = str(email_subject),
                            text = str(email_text),)
                masteruser_instance.user_logs = new_log
                masteruser_instance.save()
                return HttpResponseRedirect(reverse('commonuser:list'))
        else:
            email_form = EmailForm()

            return render(request,'commonuser/emailform.html',
                                  {'form':email_form,})


@login_required
@commonuser_required
def CommonUserUpdateView(request,slug):
    commonuser_user = get_object_or_404(UserModel,slug = slug)
    if request.user == commonuser_user :
        user_update_form = UserUpdateForm(request.POST or None, instance = commonuser_user)
        commonuser = get_object_or_404(CommonUserModel, user = commonuser_user)
        commonuser_update_form = CommonUserUpdateForm(request.POST or None, instance = commonuser)
        if commonuser_update_form.is_valid() and user_update_form.is_valid():
            user_update_form.save()
            commonuser_update_form.save()
            if 'picture' in request.FILES:
               commonuser.picture = request.FILES['picture']
               commonuser.save()
            return HttpResponseRedirect(reverse('commonuser:profile',
                                        kwargs={'slug':commonuser_user.slug}))
        return render(request,'commonuser/commonuserupdate.html',
                              {'commonuserform':commonuser_update_form,
                               'userform':user_update_form,})
    else:
        return HttpResponseRedirect(reverse('login'))


@login_required
@commonuser_required
def CommonUserDashboardView(request,slug):
    commonuser_user = get_object_or_404(UserModel,slug = slug)
    if request.user == commonuser_user:
        commonuser = get_object_or_404(CommonUserModel,user = commonuser_user)
        bookings = BookingModel.objects.filter(booker = commonuser).order_by('session__day','session__time')
        contracts = ContractModel.objects.filter(booker = commonuser).order_by('created_at_date','created_at_time')
        today = jdatetime.datetime.now().date()
        now = datetime.datetime.now().time()
        return render(request,'commonuser/dashboard.html',{'commonuser':commonuser,'bookings':bookings,
                                                            'today':today,'now':now,'contracts':contracts})
    else:
        return HttpResponseRedirect(reverse('login'))
