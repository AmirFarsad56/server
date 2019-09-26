from django.contrib import admin
from salon.models import SalonModel, SalonPictureModel
from session.models import SessionCategoryModel
from booking.models import ContractModel, BookingModel

class SalonPictureModelInline(admin.StackedInline):
    model = SalonPictureModel
    can_delete = True
    verbose_name_plural = 'SalonPictureModel'
    fk_name = 'salon'

class SessionCategoryModelInline(admin.StackedInline):
    model = SessionCategoryModel
    can_delete = True
    verbose_name_plural = 'SessionCategoryModel'
    fk_name = 'salon'

class LastDataModelInline(admin.StackedInline):
    model = SessionCategoryModel
    can_delete = True
    verbose_name_plural = 'LastDataModel'
    fk_name = 'salon'

class SalonAdmin(admin.ModelAdmin):
    list_display = ('is_confirmed','area','profit_percentage', 'company_discount_percentage', )
    list_filter = ('is_confirmed','profit_percentage', 'company_discount_percentage', )    
    search_fields = ('is_confirmed','area','profit_percentage', 'company_discount_percentage', )
    inlines = [SalonPictureModelInline,SessionCategoryModelInline, LastDataModelInline]


admin.site.register(SalonModel,SalonAdmin)
