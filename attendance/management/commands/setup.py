import os
from io import TextIOWrapper

from decouple import config
from django.core.files.uploadedfile import SimpleUploadedFile
from django.core.management import call_command
from django.core.management.base import BaseCommand

from attendance.utility import handle_uploaded_file


class Command(BaseCommand):
    help = "Set up p4k attendance - ONLY RUN ONCE!!"

    def add_arguments(self, parser):
        parser.add_argument('--mode', type=str, help="Mode")

    def handle(self, *args, **options):

        newdb = False

        self.stdout.write('Setting up Partnership 4 Kids Attendance System.')
        should_continue = input('Do you want to create a fresh DB? [y/N]?')
        if should_continue.lower() != 'y':
            self.stdout.write('Keeping existing DB')
        else:
            self.stdout.write('Removing existing DB')
            if (config('DB').lower() == 'sqlite'):
                if os.path.exists('db.sqlite3'):
                    os.remove("db.sqlite3")
                    self.stdout.write('SQL LITE DB REMOVED')

                    newdb = True
                else:
                    self.stdout.write('sqlite db not found')
            else:
                self.stdout.write( "DB Configured to {}".format( config('DB') ) )

        if not newdb:
            should_continue = input('Do you want to create and apply migrations? [y/N]?')
        else:
            should_continue = 'y' #it was a new db, so force this!

        if should_continue.lower() != 'y':
            self.stdout.write('Not applying migrations')
        else:
            migration_dir = 'attendance/migrations'
            for f in os.listdir(migration_dir):
                if f.startswith('__'):
                    continue
                self.stdout.write(f)

                os.remove(os.path.join(migration_dir, f))

            call_command("makemigrations", interactive=False)
            call_command("migrate", interactive=False)

        should_continue = input('Do you want to import sample data? [y/N]?')
        if should_continue.lower() != 'y':
            self.stdout.write('Not importing data')
        else:
            schools_file = 'attendance/tests/samples/schools.csv'
            if not os.path.exists(schools_file):
                self.stdout.write('School file not found')
            else:
                with open(schools_file, 'rb') as infile:
                    _file = SimpleUploadedFile(schools_file, infile.read())
                    result = handle_uploaded_file('school', TextIOWrapper(_file.file))
                    if result['status'] == 'success':
                        self.stdout.write('School file imported, importing classrooms and students')
                        student_file = 'attendance/tests/samples/students.csv'
                        if not os.path.exists(student_file):
                            self.stdout.write('Student import file not found')
                        else:
                            with open(student_file, 'rb') as infile:
                                _file = SimpleUploadedFile(student_file, infile.read())
                                result = handle_uploaded_file('student', TextIOWrapper(_file.file))
                                if result['status'] == 'success':
                                    self.stdout.write('Students and classrooms file imported')
                                else:
                                    self.stdout.write('Error importing students and classrooms')
                    else:
                        self.stdout.write('Error import schools, skipping student/classroom import')

        if not newdb:
            should_continue = input('Do you want to create superuser account? [y/N]?')
        else:
            should_continue = 'y' #it was a new db, so force this!

        if should_continue.lower() != 'y':
            self.stdout.write('Not create superuser account')
        else:
            self.stdout.write('Creating superuser')
            call_command("createsuperuser")

        self.stdout.write('Setup complete.')
