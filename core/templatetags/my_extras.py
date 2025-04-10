from django import template
from core.data import *

register = template.Library()

@register.filter(name='get_master_name')
def get_master_name(master_id):
    for master in masters:
        if master['id'] == master_id:
            return master['name']
    return 'Мастер не найден'