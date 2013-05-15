from django import template
from datetime import date

register = template.Library()

@register.filter(name='countdays')
def countdays(start, finish):
    return (finish - start).days * 3

@register.filter(name='add')
def add(value, addition):
    return value + addition

@register.filter(name='multiply')
def multiply(value, multiplier):
    return value * multiplier

@register.filter(name="drawdays")
def drawdays(start, finish):
    num_days = (finish - start).days
    blocks = []

    for x in range(0,num_days+1):
        blocks.append(start.day+x)

    return blocks