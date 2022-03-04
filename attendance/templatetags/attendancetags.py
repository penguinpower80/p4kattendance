from django import template

register = template.Library()


@register.simple_tag()
def version():
    return '0.0.1'
