from django import template

register = template.Library()


@register.filter(name='transform_date')
def transform_date(value):
    return value.strftime('%Y-%m-%d')