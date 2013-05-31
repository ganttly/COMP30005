from django import template
from datetime import date, datetime, timedelta

register = template.Library()

@register.filter(name='countdays')
def countdays(start, finish):
    diff = (finish - start)
    if hasattr(diff, 'days'):
        return diff.days
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

    blocks = []

    if hasattr(start, 'day'):
        first = datetime(start.year, start.month, start.day, 0, 0, 0)
        diff = (finish - start)
        num_days = 0

        if hasattr(diff, 'days'):
            num_days = (finish - start).days

        for x in range(0,num_days+2):
            #blocks.append(start.day+x)
            blocks.append(first.day)
            first += timedelta(days=1)

    return blocks

@register.filter(name="drawmonths")
def drawmonths(start, finish):
    blocks = []

    if hasattr(start, 'day'):
        day = datetime(start.year, start.month, start.day, 0, 0, 0)
        diff = (finish - start)
        num_days = 0

        blocks.append(day.strftime('%B'))
        can_append = False

        if hasattr(diff, 'days'):
            num_days = (finish - start).days

        for x in range(0,num_days+1):
            if day.day == 1 and can_append:
                blocks.append(day.strftime('%B'))
            elif(can_append):
                blocks.append("")

            can_append = True

            day += timedelta(days=1)

    return blocks

@register.filter(name="is_overdue")
def is_overdue(check_date):

    return check_date < date.today()