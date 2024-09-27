# custom_filters.py
from django import template

register = template.Library()

@register.filter
def get_item(dictionary, key):
    """Get an item from a dictionary."""
    return dictionary.get(key)



@register.filter(name='dict_get')
def dict_get(dictionary, key):
    return dictionary.get(key)

@register.filter
def dict_get(d, key):
    return d.get(key, None)


@register.filter
def get_answer(question, option_number):
    if option_number == 1:
        return question.option1
    elif option_number == 2:
        return question.option2
    elif option_number == 3:
        return question.option3
    elif option_number == 4:
        return question.option4
    return "Invalid option"


@register.filter
def dict_get(d, key):
    if isinstance(d, dict):  # Ensure 'd' is a dictionary
        return d.get(key, None)
    return None  