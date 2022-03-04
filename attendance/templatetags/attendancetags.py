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
        if this_host == 'heroku':
            checkfile = path.join(settings.BASE_DIR, 'manage.py')
            if path.exists(checkfile):
                try:
                    with open(checkfile) as reader:
                        last_deployed = path.getctime(checkfile)
                except Exception as e:
                    last_deployed = '[unable to open file]'
            else:
                last_deployed = '[check file not found]'
        else:
            last_deployed = 'Environment: ' + this_host
    except AttributeError as e:
        last_deployed = '[HOSTING not set in .env]'
    return last_deployed
