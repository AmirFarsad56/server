from django import template
from django.shortcuts import get_object_or_404
from sportclub.models import SportClubModel

register = template.Library()

@register.filter(name='pk_to_str')
def pk_to_str(pk):
    str_1 = 'gis'+str(pk)
    return str_1


@register.filter(name='pk_to_map_init')
def pk_to_str(pk):
    str_1 = 'map_init_'+str(pk)
    return str_1
