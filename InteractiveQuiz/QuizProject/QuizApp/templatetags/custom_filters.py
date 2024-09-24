# custom_filters.py
from django import template

register = template.Library()

@register.filter
def get_item(dictionary, key):
    """Get an item from a dictionary."""
    return dictionary.get(key)

register = template.Library()

@register.filter(name='dict_get')
def dict_get(dictionary, key):
    return dictionary.get(key)