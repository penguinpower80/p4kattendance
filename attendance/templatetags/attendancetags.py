import logging
from datetime import datetime
from os import path

from decouple import config
from django import template
from django.conf import settings

register = template.Library()


@register.simple_tag()
def version():
    last_deployed = ''
    try:
        this_host = config('HOSTING', default='LOCAL')
        if this_host == 'HEROKU':
            checkfile = path.join(settings.BASE_DIR, 'manage.py')
            if path.exists(checkfile):
                try:
                    with open(checkfile) as reader:
                        last_deployed = path.getctime(checkfile)
                        return datetime.fromtimestamp( last_deployed ).strftime('%m/%d/%Y %H:%M:%S')
                except Exception as e:
                    last_deployed = '[unable to open file]'
            else:
                last_deployed = '[check file not found]'
        else:
            last_deployed = 'Environment: ' + this_host
    except AttributeError as e:
        last_deployed = '[HOSTING not set in .env]'
    return last_deployed

@register.simple_tag(takes_context=True)
def current_view_class(context):
    classes = []
    logging.warning(context.request.user)
    if context.request.user.is_anonymous:
        classes.append("user-anonymous")
    if context.request.user.is_superuser:
        classes.append("user-sysadmin")

    if context.request.path == '/':
        classes.append("page-home")
    else:
        classes.append( 'page-' + context.request.path[1:].replace('/','-') )

    return " ".join(classes)

@register.simple_tag()
def status_class( status ):
    if status == 'error':
        return 'is-danger'
    if status == 'success':
        return 'is-success'
    return 'is-info'

'''
https://stackoverflow.com/questions/1906129/dict-keys-with-spaces-in-django-templates
Get a value from a dictionary with key that has a space
'''
@register.filter(name='getkey')
def getkey(value, arg):
    return value[arg]