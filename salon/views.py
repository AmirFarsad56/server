from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.shortcuts import get_object_or_404
from django.views.generic import DetailView, ListView, TemplateView
from django.forms import modelformset_factory
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.core.paginator import Paginator
from django.shortcuts import get_list_or_404
import jdatetime

#handmade
from accounts.models import UserModel
from salon.filters import SalonFilter
from company.filters import ReckoningFilter
from sportclub.models import SportClubModel
from salon.forms import SalonForm, SalonPictureForm, SalonProfitDiscountForm, SalonPictureUpdateForm
from salon.models import SalonModel, SalonPictureModel
from sportclub.decorators import sportclub_required
from accounts.decorators import superuser_required
from masteruser.decorators import masteruser_required
from booking.models import ProfitPercentageModel
from session.models import SessionModel
from booking.models import BookingModel
from company.models import ReckoningModel


#recaptcha
import json
import urllib
from django.conf import settings
from django.contrib import messages




@login_required
@sportclub_required
def SalonCreateView(request,slug):
    user = get_object_or_404(UserModel, slug=slug)
    sportclub = get_object_or_404(SportClubModel, user = user)
    if sportclub == request.user.sportclubs:

        imageformset = modelformset_factory(SalonPictureModel,
                                            form=SalonPictureForm, extra=4)
        if request.method == 'POST':
            salon_form = SalonForm(data = request.POST)
            formsets = imageformset(request.POST or None, request.FILES or None)
            if salon_form.is_valid() and formsets.is_valid():

                salon = salon_form.save(commit=False)
                #sportclub = get_object_or_404(SportClubModel, slug=slug)
                salon.sportclub = sportclub
                profit_percentage = ProfitPercentageModel.objects.get()
                salon.profit_percentage = profit_percentage.profit_percentage
                salon.save()
                for formset in formsets.cleaned_data:
                    if formset:
                        picture = formset['picture']
                        photo = SalonPictureModel(salon = salon, picture = picture)
                        photo.save()
                return HttpResponseRedirect(reverse('sportclub:workspace',
                                            kwargs={'slug':user.slug}))
            else:
                print(salon_form.errors)
        else:
            salon_form = SalonForm()
            formsets = imageformset(queryset=SalonPictureModel.objects.none())
    else:
        return HttpResponseRedirect(reverse('login'))
    return render(request,'salon/createsalon.html',
                  {'salon_form':salon_form,
                  'formsets':formsets})


@login_required
@superuser_required
def SalonSetProfitPercentage(request,pk):
    salon = get_object_or_404(SalonModel, pk = pk)
    if request.user.is_superuser:
        set_profit_form = SalonProfitDiscountForm(request.POST or None, instance = salon)
        if set_profit_form.is_valid():
            set_profit_form.save()
            salon.save()
            return HttpResponseRedirect(reverse('sportclub:detailforsuperuser',
                                                kwargs={'slug':salon.sportclub.user.slug}))
        return render(request,'salon/setprofitpercentage.html',
                              {'form':set_profit_form,})
    else:
        return HttpResponseRedirect(reverse('login'))


@login_required
@sportclub_required
def SalonUpdateView(request,slug,pk):
    sportclub_user = get_object_or_404(UserModel, slug = slug)
    sportclub = get_object_or_404(SportClubModel, user = sportclub_user)
    salon = get_object_or_404(SalonModel, pk = pk)
    if salon.sportclub == sportclub:

        salon_update_form = SalonForm(request.POST or None, instance = salon)
        if salon_update_form.is_valid():
            salon_update_form.save()
            salon.is_confirmed = False
            salon.save()
            return HttpResponseRedirect(reverse('sportclub:workspace',
                                        kwargs={'slug':slug,}))
        return render(request,'salon/updatesalon.html',
                              {'form':salon_update_form,
                              'salon':salon,})
    else:
        return HttpResponseRedirect(reverse('login'))


@method_decorator([login_required, sportclub_required], name='dispatch')
class SalonDetailView(DetailView):
    model = SalonModel
    context_object_name = 'salon_detail'
    template_name = 'salon/salondetail.html'

    def get_queryset(self):
        return SalonModel.objects.filter(sportclub = self.request.user.sportclubs)


@login_required
@masteruser_required
def ConfirmedSalonListView(request):
    salon_list = SalonModel.objects.all()
    salon_filter = SalonFilter(request.GET,queryset = salon_list)
    paginator = Paginator(salon_filter.qs, 20)
    page = request.GET.get('page')
    salons = paginator.get_page(page)
    return render(request,'salon/confirmedsalonlist.html',{'salons':salons,'filter':salon_filter})


@login_required
@masteruser_required
def UnConfirmedSalonListView(request):
    salon_list = SalonModel.objects.all()
    salon_filter = SalonFilter(request.GET,queryset = salon_list)
    paginator = Paginator(salon_filter.qs, 20)
    page = request.GET.get('page')
    salons = paginator.get_page(page)
    return render(request,'salon/unconfirmedsalonlist.html',{'salons':salons,'filter':salon_filter})


@login_required
@superuser_required
def SalonListSuperUserView(request):
    salon_list = SalonModel.objects.all()
    salon_filter = SalonFilter(request.GET,queryset = salon_list)
    paginator = Paginator(salon_filter.qs, 20)
    page = request.GET.get('page')
    salons = paginator.get_page(page)
    return render(request,'salon/salonlistforsuperuser.html',{'salons':salons,'filter':salon_filter})


@login_required
@masteruser_required
def SalonDeleteView(request,pk):
    if request.user.is_masteruser:
        salon = get_object_or_404(SalonModel,pk = pk)
        sessions = get_list_or_404(SessionModel, salon = salon)
        today = jdatetime.datetime.now().date()

        for session in sessions:
            print(session.day , session.day > today)
            if session.day > today and session.is_booked:
                return HttpResponseRedirect(reverse('salon:bookedsessionerror',pk = salon.pk))
        masteruser_instance = get_object_or_404(UserModel, slug = request.user.slug)
        masteruser_instance_logs = masteruser_instance.user_logs
        now = jdatetime.datetime.now()
        dtime = str(now.year)+'-'+str(now.month)+'-'+ str(now.day)+'  '+str(now.hour)+':'+str(now.minute)+':'+str(now.second)
        new_log = '''{previous_logs}\n
On {date_time}:\n
Deleted Salon: {salon}
Related to Sport Club: {sportclub}
-------------------------------------------------------
        '''.format(previous_logs = masteruser_instance_logs,
                   date_time = dtime,
                    salon = str(salon),
                    sportclub = str(salon.sportclub.user.username))
        masteruser_instance.user_logs = new_log
        masteruser_instance.save()
        salon.delete()
        return HttpResponseRedirect(reverse('salon:unconfirmedsalonlist'))
    else:
        return HttpResponseRedirect(reverse('login'))


@login_required
@masteruser_required
def SalonConfirmView(request,pk):
    if request.user.is_masteruser:
        salon = get_object_or_404(SalonModel,pk = pk)
        related_user = salon.sportclub.user
        if salon.sportclub.user.is_active:
            if True:
                salon.confirm()
                masteruser_instance = get_object_or_404(UserModel, slug = request.user.slug)
                masteruser_instance_logs = masteruser_instance.user_logs
                now = jdatetime.datetime.now()
                dtime = str(now.year)+'-'+str(now.month)+'-'+ str(now.day)+'  '+str(now.hour)+':'+str(now.minute)+':'+str(now.second)
                new_log = '''{previous_logs}\n
On {date_time}:\n
Confirmed Salon: {salon}
Related to Sport Club: {sportclub}
-------------------------------------------------------
                '''.format(previous_logs = masteruser_instance_logs,
                           date_time = dtime,
                            salon = str(salon),
                            sportclub = str(salon.sportclub.user.username))
                masteruser_instance.user_logs = new_log
                masteruser_instance.save()
                return HttpResponseRedirect(reverse('sportclub:detail',
                                                    kwargs={'slug':salon.sportclub.user.slug}))
            else:
                return HttpResponseRedirect(reverse('sportclub:noaccountdetailerror'))
        else:
            return HttpResponseRedirect(reverse('sportclub:bannedsportclubexception',
                                                kwargs={'slug':related_user.username}))

    else:
        return HttpResponseRedirect(reverse('login'))


@login_required
@masteruser_required
def SalonConfirmView_2(request,pk):
    if request.user.is_masteruser:
        salon = get_object_or_404(SalonModel,pk = pk)
        related_user = salon.sportclub.user
        if salon.sportclub.user.is_active:
            salon.confirm()
            masteruser_instance = get_object_or_404(UserModel, slug = request.user.slug)
            masteruser_instance_logs = masteruser_instance.user_logs
            now = jdatetime.datetime.now()
            dtime = str(now.year)+'-'+str(now.month)+'-'+ str(now.day)+'  '+str(now.hour)+':'+str(now.minute)+':'+str(now.second)
            new_log = '''{previous_logs}\n
On {date_time}:\n
Confirmed Salon: {salon}
Related to Sport Club: {sportclub}
-------------------------------------------------------
            '''.format(previous_logs = masteruser_instance_logs,
                       date_time = dtime,
                        salon = str(salon),
                        sportclub = str(salon.sportclub.user.username))
            masteruser_instance.user_logs = new_log
            masteruser_instance.save()
            return HttpResponseRedirect(reverse('salon:unconfirmedsalonlist'))
        else:
            return HttpResponseRedirect(reverse('sportclub:bannedsportclubexception',
                                                kwargs={'slug':related_user.username}))

    else:
        return HttpResponseRedirect(reverse('login'))



@login_required
@masteruser_required
def SalonBanView(request,pk):
    if request.user.is_masteruser:
        salon = get_object_or_404(SalonModel,pk = pk)
        salon.ban()
        masteruser_instance = get_object_or_404(UserModel, slug = request.user.slug)
        masteruser_instance_logs = masteruser_instance.user_logs
        now = jdatetime.datetime.now()
        dtime = str(now.year)+'-'+str(now.month)+'-'+ str(now.day)+'  '+str(now.hour)+':'+str(now.minute)+':'+str(now.second)
        new_log = '''{previous_logs}\n
On {date_time}:\n
Banned Salon: {salon}
Related to Sport Club: {sportclub}
-------------------------------------------------------
        '''.format(previous_logs = masteruser_instance_logs,
                   date_time = dtime,
                    salon = str(salon),
                    sportclub = str(salon.sportclub.user.username))
        masteruser_instance.user_logs = new_log
        masteruser_instance.save()
        return HttpResponseRedirect(reverse('sportclub:detail',
                                            kwargs={'slug':salon.sportclub.user.slug}))
    else:
        return HttpResponseRedirect(reverse('login'))


@login_required
@masteruser_required
def SalonBanView_2(request,pk):
    if request.user.is_masteruser:
        salon = get_object_or_404(SalonModel,pk = pk)
        salon.ban()
        masteruser_instance = get_object_or_404(UserModel, slug = request.user.slug)
        masteruser_instance_logs = masteruser_instance.user_logs
        now = jdatetime.datetime.now()
        dtime = str(now.year)+'-'+str(now.month)+'-'+ str(now.day)+'  '+str(now.hour)+':'+str(now.minute)+':'+str(now.second)
        new_log = '''{previous_logs}\n
On {date_time}:\n
Banned Salon: {salon}
Related to Sport Club: {sportclub}
-------------------------------------------------------
        '''.format(previous_logs = masteruser_instance_logs,
                   date_time = dtime,
                    salon = str(salon),
                    sportclub = str(salon.sportclub.user.username))
        masteruser_instance.user_logs = new_log
        masteruser_instance.save()
        return HttpResponseRedirect(reverse('salon:confirmedsalonlist'))
    else:
        return HttpResponseRedirect(reverse('login'))



@login_required
@masteruser_required
def SalonDetailViewMasterUser(request,pk):
    if request.user.is_masteruser:
        salon = get_object_or_404(SalonModel,pk = pk)
        return render(request,'salon/salondetail_masteruser.html',
                          {'salon_detail':salon})
    else:
        return HttpResponseRedirect(reverse('login'))

def SalonPictureUpdateView(request, pk):
    pic = SalonPictureModel.objects.get(pk=pk) # or with get_object_or_404
    if request.user == pic.salon.sportclub.user:
        form = SalonPictureUpdateForm(request.POST or None,instance=pic)
        if form.is_valid():
            form.save()
            if 'picture' in request.FILES:
                pic.picture = request.FILES['picture']

            pic.save()
            return HttpResponseRedirect(reverse('salon:update',
                                        kwargs={'slug':pic.salon.sportclub.user.slug,
                                                'pk':pic.salon.pk}))
        else:
            print(form.errors)
        return render(request, 'salon/salonpictureupdate.html', {'form':form})
    else:
        return HttpResponseRedirect(reverse('login'))


def SalonPictureAddView(request, pk):
    salon = SalonModel.objects.get(pk=pk)
    if request.user == salon.sportclub.user:
        if request.method == 'POST':
            form = SalonPictureUpdateForm(data = request.POST)
            if form.is_valid():
                pic = form.save(commit = False)
                pic.salon = salon
                if 'picture' in request.FILES:
                    pic.picture = request.FILES['picture']
                pic.save()
                return HttpResponseRedirect(reverse('salon:update',
                                            kwargs={'slug':salon.sportclub.user.slug,
                                                    'pk':salon.pk}))
        else:
            form = SalonPictureUpdateForm()
        return render(request, 'salon/salonpictureupdate.html', {'form':form})
    else:
        return HttpResponseRedirect(reverse('login'))


def SalonAccountingDetailView(request,pk):
    if request.user.is_sportclub or request.user.is_superuser:
        salon = get_object_or_404(SalonModel,pk = pk)
        need_to_pay = 0
        paid = 0
        total_pure_profit = 0
        pure_profit_this_round = 0
        for booking_instance in salon.bookings.all():
            if not booking_instance.transfered_to_sportclub:
                need_to_pay += booking_instance.sportclub_portion
                pure_profit_this_round += booking_instance.company_portion
            else:
                paid += booking_instance.sportclub_portion
                total_pure_profit += booking_instance.company_portion


        for booking_instance in salon.bookings.all():
            if not booking_instance.transfered_to_sportclub:
                if not booking_instance.is_contract:
                    if booking_instance.session.day < today:
                        need_to_pay += booking_instance.sportclub_portion
                        pure_profit_this_round += booking_instance.company_portion

                else:
                    if booking_instance.cancelled and booking_instance.session.day < today:
                        paid_1 = booking_instance.final_price * (100-booking_instance.profit_percentage)/100
                        difference = booking_instance.pay_back + booking_instance.sportclub_portion - (paid_1)
                        need_to_pay += difference
                        pure_profit_this_round += booking_instance.company_portion - (booking_instance.final_price * (booking_instance.profit_percentage)/100)

            else:
                paid += booking_instance.sportclub_portion
                total_pure_profit += booking_instance.company_portion

        for contract_instance in salon.contracts.all():
            if not contract_instance.transfered_to_sportclub:
                if contract_instance.created_at_date < today:
                    need_to_pay += contract_instance.sportclub_portion
                    pure_profit_this_round += contract_instance.company_portion
        return render(request,'salon/accountingdetail.html',{'need_to_pay':need_to_pay,
                                                            'total_pure_profit':total_pure_profit,
                                                            'paid':paid, 'pk':salon.pk,
                                                            'pure_profit_this_round':pure_profit_this_round})
    else:
        return HttpResponseRedirect(reverse('login'))


def SalonReckoningView(request,pk):
    if request.user.is_superuser:
        import jdatetime
        import datetime
        salon = get_object_or_404(SalonModel,pk = pk)
        need_to_pay = 0
        today = jdatetime.datetime.now().date()
        time = datetime.datetime.now().time()
        reckoning_object = ReckoningModel.objects.create(money_transfered = 0,transfered_at_date = today,
                                                        transfered_at_time = time, salon = salon)
        for booking_instance in salon.bookings.all():
            if not booking_instance.transfered_to_sportclub:
                if not booking_instance.is_contract:
                    if booking_instance.session.day < today:
                        need_to_pay += booking_instance.sportclub_portion
                        booking_instance.reckoning = reckoning_object
                        booking_instance.transfer_to_sportclub()
                        booking_instance.save()
                else:
                    if booking_instance.cancelled and booking_instance.session.day < today:
                        paid_1 = booking_instance.final_price * (100-booking_instance.profit_percentage)/100
                        difference = booking_instance.pay_back + booking_instance.sportclub_portion - (paid_1)
                        need_to_pay += difference
                        booking_instance.reckoning = reckoning_object
                        booking_instance.transfer_to_sportclub()
                        booking_instance.save()

        for contract_instance in salon.contracts.all():
            if not contract_instance.transfered_to_sportclub:
                if contract_instance.created_at_date < today:
                    need_to_pay += contract_instance.sportclub_portion
                    contract_instance.reckoning = reckoning_object
                    contract_instance.transfer_to_sportclub()
                    contract_instance.save()
                    for booking_instance_2 in contract_instance.bookings.all():
                        booking_instance.reckoning = reckoning_object
                        booking_instance.transfer_to_sportclub()
                        booking_instance.save()





        reckoning_object.money_transfered = need_to_pay
        reckoning_object.save()

        return HttpResponseRedirect(reverse('salon:accountingdetail',kwargs={'pk':salon.pk}))
    else:
        return HttpResponseRedirect(reverse('login'))



def SalonReckoninglistView(request,pk):
    if request.user.is_sportclub or request.user.is_superuser:
        salon = get_object_or_404(SalonModel,pk = pk)
        reckoning_list = ReckoningModel.objects.filter(salon = salon).order_by('-transfered_at_date','-transfered_at_time')
        reckoning_filter = ReckoningFilter(request.GET,queryset = reckoning_list)
        paginator = Paginator(reckoning_filter.qs, 20)
        page = request.GET.get('page')
        reckonings = paginator.get_page(page)
        return render(request,'salon/reckoninglist.html',{'reckonings':reckonings, 'filter':reckoning_filter})


def SalonPublicListView(request):
    salon_list = SalonModel.objects.filter(is_confirmed = True)
    salon_filter = SalonFilter(request.GET,queryset = salon_list)
    paginator = Paginator(salon_filter.qs, 10)
    page = request.GET.get('page')
    salons = paginator.get_page(page)
    return render(request,'salon/publiclist.html',{'salons':salons,'filter':salon_filter})


def SalonPublicListForSpecificSportClubView(request,pk):
    sportclub = get_object_or_404(SportClubModel,pk = pk)
    if sportclub.user.is_active:
        try:
            salon_list = SalonModel.objects.filter(is_confirmed = True, sportclub = sportclub)
            salon_filter = SalonFilter(request.GET,queryset = salon_list)
            paginator = Paginator(salon_filter.qs, 10)
            page = request.GET.get('page')
            salons = paginator.get_page(page)
            filter_off = False
            if len(salon_list) == 1:
                filter_off = True
            return render(request,'salon/publiclistforsportclub.html',{'filter_off':filter_off,'salons':salons,'filter':salon_filter,'sportclub':sportclub})
        except:
            return render(request,'salon/publiclistforsportclub.html')
    else:
        return HttpResponseRedirect(reverse('sportclub:publicdetail',kwargs={'pk':sportclub.pk}))
