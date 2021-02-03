from django import template
from core import models

register = template.Library()


@register.filter
def cart_item_count(user):
    if user.is_authenticated:
        
        qs = models.Order.objects.filter(user=user, ordered=False).first()
        if qs:
            return qs.item.count()
    return 0
