from random import randint
from django import template

register = template.Library()

@register.simple_tag
def random_int(a, b=None):
    if b is None:
        a, b = 0, a
    return randint(a, b)

@register.simple_tag
def get_random_img():
    return f'/static/registration/imgs/background ({randint(1,21)}).jpg'