from django.contrib.auth.models import Group, User
from django.core.management.base import BaseCommand
from faker import Faker


class Command(BaseCommand):
    help = "Create some facilitators."

    def add_arguments(self, parser):
        parser.add_argument('--mode', type=str, help="Mode")

    def handle(self, *args, **options):
        num_mentors = int(input('How many facilitators?'))
        try:
            group = Group.objects.get(name='Facilitators')
        except Group.DoesNotExist:
            self.stdout.write('Facilitators group does not exist')
            exit()

        faker = Faker()

        for x in range(0, num_mentors):
            fname = faker.unique.first_name()
            lname = faker.unique.last_name()
            username = fname[0].lower() + lname.lower()
            email = username + "@p4kids.org"
            password = faker.password(length=15)
            u = User.objects.create_user(username=username, password=password, first_name=fname, last_name=lname,
                                         is_staff=0, is_superuser=0, last_login=None, email=email)
            group.user_set.add(u)

        self.stdout.write("Finished adding facilitators")
