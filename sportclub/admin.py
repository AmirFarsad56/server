from django.contrib import admin
from sportclub.models import SportClubModel
from salon.models import SalonModel
from leaflet.admin import LeafletGeoAdmin

class SalonModelInline(admin.StackedInline):
    model = SalonModel
    can_delete = True
    verbose_name_plural = 'SalonModel'
    fk_name = 'sportclub'

class SportClubAdmin(LeafletGeoAdmin):
    inlines = [SalonModelInline,]


admin.site.register(SportClubModel,SportClubAdmin)
