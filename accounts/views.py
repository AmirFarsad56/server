from django.shortcuts import render
from django.views.generic import DetailView, UpdateView
from django.conf import settings
from django.urls import reverse_lazy, reverse
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.shortcuts import get_object_or_404
from django.urls import reverse
import jdatetime
import datetime
from django.http import HttpResponseRedirect
from django.contrib.auth.password_validation import validate_password, MinimumLengthValidator
from django.contrib.auth import authenticate, login
import random
from django.conf import settings

#handmade
from accounts.models import UserModel
from accounts.decorators import superuser_required
from accounts.forms import (EmailForm, MessageForm, TypesForm,
                            SuperUserUpdateForm, PasswordChangeForm, ForgotPasswordForm)
from commonuser.models import CommonUserModel
from sportclub.models import SportClubModel
from masteruser.models import MasterUserModel
from booking.models import ProfitPercentageModel
from company.models import TermsModel, SalonAdvertisementModel

#Email send
from django.core.mail import send_mail

#SMS send
from django.utils import timezone
from kavenegar import KavenegarAPI


@login_required
@superuser_required
def SuperUserProfileView(request,slug):
    user = get_object_or_404(UserModel , slug = slug)
    if user.username == request.user.username:
        profit_percantage = ProfitPercentageModel.objects.all()
        terms_condition = TermsModel.objects.all()
        return render(request, 'accounts/superuserprofile.html', {'superuser':user,
                        'profit_percantage':profit_percantage,'terms':terms_condition})
    else:
        return HttpResponseRedirect(reverse('login'))


@login_required
@superuser_required
def SuperUserWorkSpaceView(request,slug):
    user = get_object_or_404(UserModel , slug = slug)
    if user.username == request.user.username:
        profit_percantage = ProfitPercentageModel.objects.all()
        terms_condition = TermsModel.objects.all()
        salonadvertisement = SalonAdvertisementModel.objects.all()
        return render(request, 'accounts/workspace.html', {'superuser':user,
                        'profit_percantage':profit_percantage,'terms':terms_condition,
                        'salonadvertisement':salonadvertisement})
    else:
        return HttpResponseRedirect(reverse('login'))



@login_required
@superuser_required
def CloudMessageView(request):
    api = KavenegarAPI(settings.KAVENEGAR_API_KEY)
    if request.user.is_superuser:

        if request.method == 'POST':
            types_form = TypesForm(data = request.POST )
            message_form = MessageForm(data = request.POST)
            if message_form.is_valid() and types_form.is_valid():
                masterusers = types_form.cleaned_data['masterusers']
                sportclubs = types_form.cleaned_data['sportclubs']
                commonusers = types_form.cleaned_data['commonusers']
                message_text = message_form.cleaned_data.get('text')
                failed_to_users = ''' fails: \n '''
                success = ''' success: \n '''
                if masterusers:
                    master_users = MasterUserModel.objects.all()
                    for master_user in master_users:
                        try:
                            params = {
                            'sender': settings.KAVENEGAR_PHONE_NUMBER,
                            'receptor': master_user.phone_number,
                            'message' : message_text
                            }
                            response = api.sms_send(params)
                            success += 'masteruser- name: ' +str(master_user.user.username) +' with phone_number: ' + str(master_user.phone_number) +'\n'
                        except:
                            failed_to_users += 'masteruser- name: ' +str(master_user.user.username) +' with phone_number: ' + str(master_user.phone_number) +'\n'
                if sportclubs:
                    sport_clubs = SportClubModel.objects.all()
                    for sport_club in sport_clubs:
                        try:
                            params = {
                            'sender': settings.KAVENEGAR_PHONE_NUMBER,
                            'receptor': sport_club.phone_number,
                            'message' : message_text
                            }
                            response = api.sms_send(params)
                            success += 'sportclub- username: ' +str(sport_club.user.username) +' with phone_number: ' + str(sport_club.phone_number) +'\n'
                        except:
                            failed_to_users += 'sportclub- username: ' +str(sport_club.user.username) +' with phone_number: ' + str(sport_club.phone_number) +'\n'
                if commonusers:
                    common_users = CommonUserModel.objects.all()
                    for common_user in common_users:
                        try:
                            params = {
                            'sender': settings.KAVENEGAR_PHONE_NUMBER,
                            'receptor': common_user.phone_number,
                            'message' : message_text
                            }
                            response = api.sms_send(params)
                            success += 'commonuser- username: ' +str(common_user.user.username) +' with phone_number: ' + str(common_user.phone_number) +'\n'
                        except:
                            failed_to_users += 'commonuser- username: ' +str(common_user.user.username) +' with phone_number: ' + str(common_user.phone_number) +'\n'


                superuser_instance = get_object_or_404(UserModel, slug = request.user.slug)
                superuser_instance_logs = superuser_instance.user_logs
                to = ''
                if commonusers:
                    to += 'Common Users '
                if sportclubs:
                    to += 'Sport Clubs '
                if masterusers:
                    to += 'Master Users '
                now = jdatetime.datetime.now()
                dtime = str(now.year)+'-'+str(now.month)+'-'+ str(now.day)+'  '+str(now.hour)+':'+str(now.minute)+':'+str(now.second)
                new_log = '''{previous_logs}\n
On {date_time} \n
Sent Cloud Message To: {to}\n
Message:\n
{message}
-------------------------------------------------------
                '''.format(previous_logs = superuser_instance_logs,
                           date_time = dtime,
                            to = to,
                            message = str(message_text),)
                superuser_instance.user_logs = new_log
                superuser_instance.save()
                return render(request,'accounts/cloudmessage.html',
                                      {'failed_to_users':failed_to_users,
                                      'success':success})
        else:
            message_form = MessageForm()
            types_form = TypesForm()

            return render(request,'accounts/cloudmessage.html',
                                  {'message_form':message_form,
                                   'types_form':types_form})


@login_required
@superuser_required
def CloudEmailView(request):
    if request.user.is_superuser:
        if request.method == 'POST':
            email_form = EmailForm(data = request.POST)
            types_form = userlist = TypesForm(data = request.POST)
            if email_form.is_valid() and types_form.is_valid():
                users = UserModel.objects.all()
                email_subject = email_form.cleaned_data.get('subject')
                email_text = email_form.cleaned_data.get('text')
                masterusers = types_form.cleaned_data['masterusers']
                sportclubs = types_form.cleaned_data['sportclubs']
                commonusers = types_form.cleaned_data['commonusers']
                failed_to_users = ''' fails : \n'''
                success = ''' success : \n'''
                for user in users:
                    try:
                        if masterusers and user.is_masteruser :
                            send_mail(
                            email_subject,
                            email_text,
                            'alienone306@gmail.com',
                            [user.email,],
                            fail_silently=False,
                            )
                        if sportclubs and user.is_sportclub :
                            send_mail(
                            email_subject,
                            email_text,
                            'alienone306@gmail.com',
                            [user.email,],
                            fail_silently=False,
                            )
                        if commonusers and user.is_commonuser :
                            send_mail(
                            email_subject,
                            email_text,
                            'info@varzesh-kon.ir',
                            [user.email,],
                            fail_silently=False,
                            )
                        success += 'username: ' +str(user.username) +' with email: ' + str(user.email) +'\n'
                    except:
                        failed_to_users += 'username: ' +str(user.username) +' with email: ' + str(user.email) +'\n'

                superuser_instance = get_object_or_404(UserModel, slug = request.user.slug)
                superuser_instance_logs = superuser_instance.user_logs
                to = ''
                if commonusers:
                    to += 'Common Users '
                if sportclubs:
                    to += 'Sport Clubs '
                if masterusers:
                    to += 'Master Users '
                now = jdatetime.datetime.now()
                dtime = str(now.year)+'-'+str(now.month)+'-'+ str(now.day)+'  '+str(now.hour)+':'+str(now.minute)+':'+str(now.second)
                new_log = '''{previous_logs}\n
On {date_time}:\n
Sent Cloud Email To: {to}\n
Email Subject:
{subject}\n
Email Text:\n
{text}
-------------------------------------------------------
                '''.format(previous_logs = superuser_instance_logs,
                           date_time = dtime,
                            to = to,
                            subject = str(email_subject),
                            text = str(email_text),)
                superuser_instance.user_logs = new_log
                superuser_instance.save()
                return render(request,'accounts/cloudemail.html',
                                      {'failed_to_users':failed_to_users,
                                      'success':success})
        else:
            email_form = EmailForm()
            types_form = TypesForm()

            return render(request,'accounts/cloudemail.html',
                                  {'email_form':email_form,
                                   'types_form':types_form})


@login_required
@superuser_required
def SuperUserUpdateView(request,slug):
    superuser_user = get_object_or_404(UserModel,slug = slug)
    user_update_form = SuperUserUpdateForm(request.POST or None, instance = superuser_user)
    if user_update_form.is_valid():
        user_update_form.save()
        if 'picture' in request.FILES:
           superuser_user.picture = request.FILES['picture']
           superuser_user.save()
        return HttpResponseRedirect(reverse('accounts:profile',
                                    kwargs={'slug':superuser_user.slug}))
    return render(request,'accounts/superuserupdate.html',
                          {'userform':user_update_form,})


@login_required
def PasswordChangeView(request,slug):
    user = get_object_or_404(UserModel,slug = slug)
    if request.method == 'POST':
        password_form = PasswordChangeForm(data = request.POST)
        if password_form.is_valid():
            current_password = password_form.cleaned_data.get('current_password')
            logged_in = authenticate(request, username=user.username, password=current_password)

            if logged_in is not None:
                if password_form.cleaned_data.get('new_password') == password_form.cleaned_data.get('confirm_password'):
                    new_password = password_form.cleaned_data.get('new_password')
                    try:
                        validate_password(new_password,user=user, password_validators=None)
                        user.set_password(new_password)
                        user.save()
                        return HttpResponseRedirect(reverse('login'))
                    except:
                        error1 ='کلمه عبور باید بیش از 6 کاراکتر باشد'
                        error2 ='کلمه عبور باید نمیتواند شامل نام کاربری باشد'
                        error3 ='کلمه عبور نمیتواند خیلی ساده باشد'
                        return render(request,'accounts/passwordchange.html',{'form':password_form,'error1':error1,'error2':error2,'error3':error3})
                else:
                    error4 = 'رمز های وارد شده با هم مطابقت ندارند'
                    password_form = PasswordChangeForm()
                    return  render(request,'accounts/passwordchange.html',
                                          {'error4':error4,'form':password_form})

            else:
                error4 = 'رمزعبور وارد شده صحیح نیست'
                password_form = PasswordChangeForm()
                return  render(request,'accounts/passwordchange.html',
                                      {'error4':error4,'form':password_form})
    else:
        password_form = PasswordChangeForm()
        return  render(request,'accounts/passwordchange.html',
                              {'form':password_form})


def ForgotPasswordView(request):
    api = KavenegarAPI(settings.KAVENEGAR_API_KEY)
    try:
        last_retry_str = request.session['last_retry']
        last_retry = datetime.datetime.strptime(last_retry_str,"%Y-%m-%d %H:%M:%S")
    except:
        last_retry = datetime.datetime.now()
    now = datetime.datetime.now()
    if now >= last_retry:
        if request.method == 'POST':
            data = request.POST.copy()
            form = ForgotPasswordForm(data=request.POST)

            phone_number_exists = False
            if form.is_valid():
                phone_number = form.cleaned_data.get('phone_number')

                try :
                    commonuser = get_object_or_404(CommonUserModel,phone_number = phone_number)
                    if commonuser:
                        print(commonuser)
                        user = commonuser.user
                        var = 'abcdefghijklmnpqrstuvwxyzABCDEFIJKLMNPQRSTUVWXYZ123456789'
                        new_password=''
                        for i in range(0,random.randrange(10,13,1)):
                            c = random.choice(var)
                            new_password += c


                        params = {
                        'sender': settings.KAVENEGAR_PHONE_NUMBER,
                        'receptor': phone_number,
                        'message' : 'سامانه ورزش کن\n' + str(user.username) + ' :'+'نام کاربری شما'+'\n'+ new_password +' :'+ 'رمز عبور جدید شما '
                        }
                        response = api.sms_send(params)
                        phone_number_exists = True
                        user.set_password(new_password)
                        print(user.password)
                        user.save()
                        now = datetime.datetime.now() + datetime.timedelta(minutes=3)
                        str_now = str(now.year)+'-'+str(now.month)+'-'+str(now.day)+' '+str(now.hour)+':'+str(now.minute)+':'+str(now.second)
                        request.session['last_retry'] = str_now
                        return HttpResponseRedirect(reverse('login'))
                except:
                    pass
                try :
                    sportclub = get_object_or_404(SportClubModel,phone_number = phone_number)
                    if sportclub:
                        user = sportclub.user
                        var = 'abcdefghijklmnpqrstuvwxyzABCDEFIJKLMNPQRSTUVWXYZ123456789'
                        new_password=''
                        for i in range(0,random.randrange(10,13,1)):
                            c = random.choice(var)
                            new_password += c


                        params = {
                        'sender': settings.KAVENEGAR_PHONE_NUMBER,
                        'receptor': phone_number,
                        'message' : 'سامانه ورزش کن\n' + str(user.username) + ' :'+'نام کاربری شما'+'\n'+ new_password +' :'+ 'رمز عبور جدید شما '
                        }

                        response = api.sms_send(params)
                        phone_number_exists = True
                        user.set_password(new_password)
                        print(user.password)
                        user.save()
                        now = datetime.datetime.now() + datetime.timedelta(minutes=3)
                        str_now = str(now.year)+'-'+str(now.month)+'-'+str(now.day)+' '+str(now.hour)+':'+str(now.minute)+':'+str(now.second)
                        request.session['last_retry'] = str_now
                        return HttpResponseRedirect(reverse('login'))
                except:
                    pass
                try :
                    masteruser = get_object_or_404(MasterUserModel,phone_number = phone_number)
                    if masteruser:
                        user = masteruser.user
                        var = 'abcdefghijklmnpqrstuvwxyzABCDEFIJKLMNPQRSTUVWXYZ123456789'
                        new_password=''
                        for i in range(0,random.randrange(10,13,1)):
                            c = random.choice(var)
                            new_password += c


                        params = {
                        'sender': settings.KAVENEGAR_PHONE_NUMBER,
                        'receptor': phone_number,
                        'message' : 'سامانه ورزش کن\n' + str(user.username) + ' :'+'نام کاربری شما'+'\n'+ new_password +' :'+ 'رمز عبور جدید شما '
                        }
                        print(user.password)
                        response = api.sms_send(params)
                        phone_number_exists = True
                        user.set_password(new_password)
                        user.save()
                        now = datetime.datetime.now() + datetime.timedelta(minutes=3)
                        str_now = str(now.year)+'-'+str(now.month)+'-'+str(now.day)+' '+str(now.hour)+':'+str(now.minute)+':'+str(now.second)
                        request.session['last_retry'] = str_now
                        return HttpResponseRedirect(reverse('login'))
                except:
                    pass

            else:
                print(form.errors)
            if not phone_number_exists:
                return HttpResponseRedirect(reverse('accounts:wrongphonenumber'))


        else:
            form = ForgotPasswordForm()

        return render(request,'accounts/forgotpassword.html',{'form':form})
    else:
        return HttpResponseRedirect(reverse('commonuser:twominwait'))


def WrongPhoneNumberView(request):
    return render(request,'accounts/wrongphonenumber.html')



@login_required
@superuser_required
def DeleteInactiveUsersView(request):
    counter = 0
    for user in  UserModel.objects.all():
        if not user.is_active:
            try:
                if user.is_commonuser:
                    commonuser = user.commonusers
                    commonuser.delete()

            except:
                pass
    return HttpResponseRedirect(reverse('accounts:workspace',kwargs={'slug':request.user.slug}))
