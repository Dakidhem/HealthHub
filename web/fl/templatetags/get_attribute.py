from django import template

register = template.Library()


@register.filter(name='get_attribute')
def get_attribute(obj, attr):
    """
    Custom template filter to access dictionary values using dot notation.
    """
    try:
        return obj[attr]
    except (KeyError, TypeError):
        return None