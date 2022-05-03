import string

from decouple import config
from django.conf import settings
from django.core.mail import send_mail
from django.core.management import BaseCommand


# https://docs.djangoproject.com/en/4.0/topics/email/

class Command(BaseCommand):
    help = "Send Test Email."

    def add_arguments(self, parser):
        parser.add_argument('to', nargs='+', help="Email address to send to")
        parser.add_argument('from', help="Email address to send from")

    def handle(self, *args, **options):

        print(options)

        if options['to'] and options['from']:
            self.stdout.write('Sending test email to {} from {}'.format( options['to'], options['from']) )
        try:
            send_mail(
                'Test from p4k',
                'Here is the sample message.',
                options['from'],
                options['to'],
                fail_silently=False,
            )

            self.stdout.write('Sent using:{}'.format(settings.EMAIL))

            if (settings.EMAIL == 'LOCAL'):
                self.stdout.write('Check "/{}" for emails'.format(settings.EMAIL_FILE_PATH))

        except Exception as e:
            print( str(e) )



