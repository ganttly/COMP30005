from django import template
from datetime import date, datetime

register = template.Library()

@register.filter(name='countdays')
def countdays(start, finish):
    diff = (finish - start)
    if hasattr(diff, 'days'):
        return diff.days * 3
    else:
        return 0

@register.filter(name='add')
def add(value, addition):
    return value + addition

@register.filter(name='multiply')
def multiply(value, multiplier):
    return value * multiplier

@register.filter(name="drawdays")
def drawdays(start, finish):
    diff = (finish - start)
    num_days = 0

    if hasattr(diff, 'days'):
        num_days = (finish - start).days

    blocks = []

    for x in range(0,num_days):
        if hasattr(start, 'day'):
            blocks.append(start.day+x)

    return blocks

@register.filter(name="is_overdue")
def is_overdue(check_date):

    return check_date < datetime.now()