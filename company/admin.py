from django.contrib import admin
from company.models import TermsModel, ReckoningModel, SalonAdvertisementModel

admin.site.register(TermsModel)
admin.site.register(SalonAdvertisementModel)


class ReckoningAdmin(admin.ModelAdmin):
    list_display = ('salon','transfered_at_date','transfered_at_time','money_transfered' )
    list_filter = ('salon','transfered_at_date','transfered_at_time','money_transfered' )
    search_fields = ('salon','transfered_at_date','transfered_at_time','money_transfered' )

admin.site.register(ReckoningModel,ReckoningAdmin)
