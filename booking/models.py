from django.db import models
from django.conf import settings
from django_jalali.db import models as jmodels
import jdatetime
import datetime
from commonuser.models import CommonUserModel
from salon.models import SalonModel
from company.models import ReckoningModel

#handmade
from session.models import SessionModel


class ProfitPercentageModel(models.Model):
    profit_percentage = models.IntegerField(null = False , default = 0)


class ContractModel(models.Model):
    reckoning = models.ForeignKey(ReckoningModel, on_delete = models.PROTECT, null = True,
                                related_name='contracts')
    booker = models.ForeignKey(CommonUserModel, on_delete = models.SET_NULL, null = True,
                                related_name='contracts')
    salon = models.ForeignKey(SalonModel, on_delete = models.SET_NULL, null = True,
                                related_name='contracts')
    created_at_date = jmodels.jDateField(null = False)
    str_created_at_date = models.CharField(null = False, max_length = 264)
    created_at_time = models.TimeField(null = False)
    total_price = models.FloatField(null = False )
    transfered_to_sportclub = models.BooleanField(null = False, default = False)
    transfered_at_date = jmodels.jDateField(null = True)
    transfered_at_time = models.TimeField(null = True)
    numbers = models.IntegerField(null = False)
    sportclub_portion = models.FloatField(null = True )
    company_portion = models.FloatField(null = True )

    def transfer_to_sportclub(self):
        self.transfer_to_sportclub = True
        date = jdatetime.datetime.now().date()
        time = datetime.datetime.now().time()
        self.transfered_at_date = date
        self.transfered_at_time = time
        self.save()

    def save(self, *args, **kwargs):
        self.str_created_at_date = str(self.created_at_date)
        super(ContractModel, self).save(*args, **kwargs)


class BookingModel(models.Model):
    reckoning = models.ForeignKey(ReckoningModel, on_delete = models.PROTECT, null = True,
                                related_name='bookings')
    salon = models.ForeignKey(SalonModel, on_delete = models.SET_NULL, null = True,
                                related_name='bookings')
    session = models.ForeignKey(SessionModel, on_delete = models.SET_NULL , null = True,
                                related_name='bookings')
    booker = models.ForeignKey(CommonUserModel, on_delete = models.SET_NULL, null = True,
                                related_name='bookings')
    contract = models.ForeignKey(ContractModel, on_delete = models.SET_NULL, null = True,
                                related_name='bookings')
    transfered_to_sportclub = models.BooleanField(null = False, default = False)
    transfered_at_date = jmodels.jDateField(null = True)
    transfered_at_time = models.TimeField(null = True)
    booked_at_date = jmodels.jDateField(null = False)
    booked_at_time = models.TimeField(null = False)
    final_price = models.FloatField(null = False)
    discount_percentage = models.IntegerField(null = False)
    company_discount_percentage = models.IntegerField(null = False)
    raw_price = models.FloatField(null = False)
    profit_percantage = models.IntegerField(null = False)
    company_portion = models.FloatField(null = False)
    sportclub_portion = models.FloatField(null = False)#change this to null = False later
    cancelled = models.BooleanField(null = False, default = False)
    is_contract = models.BooleanField(null = False, default = False)
    contract_discount = models.IntegerField(null = True)
    code = models.CharField(null = False, max_length = 264)
    pay_back = models.FloatField(null = True)
    cancelled_at_date = jmodels.jDateField(null = True)
    cancelled_at_time = models.TimeField(null = True)

    def __str__(self):
        return str(self.user.username) + ' booked ' + str(self.sesison.pk)

    def transfer_to_sportclub(self):
        self.transfer_to_sportclub = True
        date = jdatetime.datetime.now().date()
        time = datetime.datetime.now().time()
        self.transfered_at_date = date
        self.transfered_at_time = time
        self.save()
