import os

from decouple import config
from django.core.management import call_command
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = "Set up p4k attendance - ONLY RUN ONCE!!"

    def add_arguments(self, parser):
        parser.add_argument('--mode', type=str, help="Mode")

    def handle(self, *args, **options):
        self.stdout.write('Setting up Partnership 4 Kids Attendance System - this should only be run once!')
        should_continue = input('Do you want to continue? [y/N]?')
        if should_continue.lower() != 'y':
            self.stdout.write('NOT continuing...')
            return
        migration_dir = 'attendance/migrations'

        if ( config('DB') == 'SQLITE'):
            if os.path.exists( 'db.sqlite3' ):
                os.remove("db.sqlite3")
            else:
                self.stdout.write('sqlite db not found')
            for f in os.listdir(migration_dir):
                if f.startswith('__'):
                    continue
                self.stdout.write(f)

                os.remove( os.path.join(migration_dir, f) )

        call_command("makemigrations", interactive=False)
        call_command("migrate", interactive=False)
        self.stdout.write('Creating superuser')
        call_command("createsuperuser")
        self.stdout.write('Setup complete.')