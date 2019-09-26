from django.contrib import admin
from booking.models import ProfitPercentageModel, BookingModel, ContractModel

admin.site.register(ProfitPercentageModel)
# Register your models here.


class BookingAdmin(admin.ModelAdmin):
    list_display = ('salon', 'transfered_to_sportclub', 'booked_at_date','transfered_at_date','final_price','company_portion','cancelled','is_contract','cancelled_at_date')
    list_filter = ('reckoning','salon','session', 'transfered_to_sportclub', 'booked_at_date','transfered_at_date','final_price','company_portion','cancelled','is_contract','cancelled_at_date')
    search_fields = ('reckoning','salon','session', 'transfered_to_sportclub', 'booked_at_date','transfered_at_date','final_price','company_portion','cancelled','is_contract','cancelled_at_date')


admin.site.register(BookingModel,BookingAdmin)


class ContractAdmin(admin.ModelAdmin):
    list_display = ('salon', 'created_at_date', 'numbers','total_price')
    list_filter = ('salon', 'created_at_date', 'numbers','total_price')
    search_fields = ('salon', 'created_at_date', 'numbers','total_price')


admin.site.register(ContractModel,ContractAdmin)
