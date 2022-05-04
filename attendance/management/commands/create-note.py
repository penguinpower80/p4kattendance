from datetime import datetime, timezone

from django.contrib.auth.models import Group, User
from django.core.management.base import BaseCommand
from django.shortcuts import get_object_or_404
from faker import Faker

from attendance.models import Classroom, Student, School, Notes


class Command(BaseCommand):
    help = "Create some notes."

    def add_arguments(self, parser):
        parser.add_argument('datetime', type=str, nargs='+', help="Date in \"mm/dd/yyyy HH:mm\" 24-hr format (WITH the double quotes)")
        parser.add_argument('--userid', type=int, help="Id of author", required=True)
        parser.add_argument('--type', type=str, help="Type of entity. S=School, C=Classroom, P=Pupil/Student", default='P')
        parser.add_argument('--id', type=str, help="Id for that Type. Defaults to Student type", required=True)
        parser.add_argument('--note', type=str, help="Note Text. Exclude to auto populate with random text.", default='AUTO')
        parser.add_argument('--visible', type=str, help="Visible or not. Set to 0 to not be visible", default='1')

    def handle(self, *args, **options):

        user = User.objects.get(pk=options['userid'])

        if options['type'] == 'P':
            student = get_object_or_404(Student, pk=options['id'])
        elif options['type'] == 'C':
            classroom = get_object_or_404(Classroom, pk=options['id'])
        elif options['type'] == 'S':
            school = get_object_or_404(School, pk=options['id'])
        else:
            raise ValueError('Invalid Type. Must be one of S, C, or P')


        for dt in options['datetime']:
            if options['note'] == 'AUTO':
                faker = Faker()
                text = faker.sentence()
            else:
                text = options['note']

            note = Notes.objects.create(
                author=user,
                type=options['type'],
                tid=options['id'],
                text=text,
                visible=options['visible'] != '0',
            )


            timestamp = datetime.strptime(dt, "%m/%d/%Y %H:%M").replace(tzinfo=timezone.utc)
            note.created_at = timestamp
            note.save()

