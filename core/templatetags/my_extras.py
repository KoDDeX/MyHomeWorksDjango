from django import template
from core.models import Master

register = template.Library()


@register.filter(name="get_master_name")
def get_master_name(master_id):
    try:
        master = Master.objects.get(id=master_id)
        return master.name
    except Master.DoesNotExist:
        return "Мастер не найден"
