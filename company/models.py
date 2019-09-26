from django.db import models
from django_jalali.db import models as jmodels
import jdatetime
import datetime
from salon.models import SalonModel


class TermsModel(models.Model):
    terms_condition = models.TextField(null = False)

    def __str__(self):
        return 'TermsAndConditionsObject ' + str(self.pk)



class ReckoningModel(models.Model):
    salon = models.ForeignKey(SalonModel, on_delete = models.SET_NULL, null = True,
                                related_name='reckonings')
    transfered_at_date = jmodels.jDateField(null = True)
    str_transfered_at_date = models.CharField(null = False, max_length = 264)
    transfered_at_time = models.TimeField(null = True)
    money_transfered = models.FloatField(null = False)

    def __str__(self):
        return str(self.pk) + 'Reckoning ' + str(self.salon.sportclub.sportclub_name)

    def save(self, *args, **kwargs):
        self.str_transfered_at_date = str(self.transfered_at_date)
        super(ReckoningModel, self).save(*args, **kwargs)


class SalonAdvertisementModel(models.Model):
    salon = models.ForeignKey(SalonModel, on_delete = models.SET_NULL, null = True,
                                related_name='advertisements')
    added_at_date = jmodels.jDateField(null = True)
    str_added_at_date = models.CharField(null = False, max_length = 264)
    added_at_time = models.TimeField(null = True)

    def save(self, *args, **kwargs):
        self.str_added_at_date = str(self.added_at_date)
        super(SalonAdvertisementModel, self).save(*args, **kwargs)
