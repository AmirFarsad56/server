from django.shortcuts import render
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.views.generic import CreateView, UpdateView, ListView
from django.urls import reverse
from django.shortcuts import get_object_or_404
from django.core.paginator import Paginator
from django.http import HttpResponseRedirect
import jdatetime
import datetime

#handmade
from company.models import TermsModel, ReckoningModel, SalonAdvertisementModel
from company.filters import ReckoningFilter
from company.forms import TermsForm
from accounts.decorators import superuser_required
from salon.models import SalonModel



@method_decorator([login_required, superuser_required], name='dispatch')
class CreateTermsView(CreateView):
    model = TermsModel
    form_class = TermsForm
    template_name = 'company/createterms.html'

    def get_success_url(self):
        return reverse('accounts:workspace',kwargs={'slug':self.request.user.slug})


@method_decorator([login_required, superuser_required], name='dispatch')
class UpdateTermsView(UpdateView):
    model = TermsModel
    form_class = TermsForm
    template_name = 'company/updateterms.html'

    def get_success_url(self):
        return reverse('accounts:workspace',kwargs={'slug':self.request.user.slug})


def AccountingDetailView(request):
    if request.user.is_superuser :
        today = jdatetime.datetime.now().date()
        need_to_pay = 0
        paid = 0
        total_pure_profit = 0
        pure_profit_this_round = 0
        for salon in SalonModel.objects.all():

            for booking_instance in salon.bookings.all():
                if booking_instance.session.day < today:
                    if not booking_instance.transfered_to_sportclub:
                        need_to_pay += booking_instance.sportclub_portion
                        pure_profit_this_round += booking_instance.company_portion
                    else:
                        paid += booking_instance.sportclub_portion
                        total_pure_profit += booking_instance.company_portion
        try:
            return render(request,'company/accountingdetails.html',{'need_to_pay':need_to_pay,
                                                                'total_pure_profit':total_pure_profit,
                                                                'paid':paid,
                                                                'pure_profit_this_round':pure_profit_this_round})
        except:
            return render(request,'company/accountingdetails.html')

    else:
        return HttpResponseRedirect(reverse('login'))


def ReckoninglistView(request):
    if request.user.is_superuser:
        reckoning_list = ReckoningModel.objects.order_by('-transfered_at_date','-transfered_at_time')
        reckoning_filter = ReckoningFilter(request.GET,queryset = reckoning_list)
        paginator = Paginator(reckoning_filter.qs, 15)
        page = request.GET.get('page')
        reckonings = paginator.get_page(page)
        return render(request,'company/reckoninglist.html',{'reckonings':reckonings,'filter':reckoning_filter})


@login_required
@superuser_required
def SalonAdvertisementCreateView(request,pk):
    salon = get_object_or_404(SalonModel,pk = pk)
    added_at_time = datetime.datetime.now().time()
    added_at_date = jdatetime.datetime.now().date()
    salonadvertisement_object  = SalonAdvertisementModel.objects.create(salon = salon, added_at_date = added_at_date,
                                                                        added_at_time = added_at_time,)
    salonadvertisement_object.save()
    return HttpResponseRedirect(reverse('accounts:workspace',kwargs={'slug':request.user.slug}))


class SalonAdvertisementListView(ListView):
    model = SalonAdvertisementModel
    template_name = 'company/salonadvertisementlist.html'
    context_object_name = 'advertisements'


@login_required
@superuser_required
def SalonAdvertisementDeleteView(request,pk):
    object = get_object_or_404(SalonAdvertisementModel,pk = pk)
    object.delete()
    return HttpResponseRedirect(reverse('company:salonadvertisementlist'))


def TermsDetailView(request):
    terms = TermsModel.objects.all()
    return render(request,'company/termsdetail.html',{'terms':terms})


def FAQsView(request):
    return render(request,'company/faqs.html')


def AboutUsView(request):
    return render(request,'company/aboutus.html')


def ContactUsView(request):
    return render(request,'company/contactus.html')
