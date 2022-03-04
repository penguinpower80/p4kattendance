import csv
import datetime
import random
from csv import reader

from faker import Faker

fake = Faker()


def fakeStudentRow(school, grade):
    hasNote = fake.boolean(chance_of_getting_true=25)
    s = datetime.date(2006,1,1)
    e = datetime.date(2020,12,31)
    return [
        fake.numerify('##########'),
        school,
        grade,
        fake.first_name(),
        fake.last_name(),
        fake.date_between(s, e),
        fake.random_element(elements=('f', 'm',)),
        fake.street_address(),
        fake.city(),
        'NE',
        fake.postcode(),
        fake.email(),
        fake.numerify('402-###-####'),
        fake.paragraph(5, True) if hasNote else ''
    ]

with open('students.csv', 'w', newline='') as csvfile:
    classeswriter = csv.writer(csvfile, delimiter=',', quotechar='"', quoting=csv.QUOTE_ALL)
    classeswriter.writerow(['NDE ID','SCHOOL ID', 'CLASSROOM', 'FIRST', 'LAST', 'DOB', 'GENDER', 'STREET','CITY', 'STATE', 'ZIP', 'EMAIL', 'PHONE', 'NOTE'])
    with open('schools.csv', 'r') as read_obj:
        # pass the file object to reader() to get the reader object
        csv_reader = reader(read_obj)
        # Iterate over each row in the csv using reader object
        classes = []
        for row in csv_reader:
            if fake.boolean():
                match row[2]:
                    case 'TYPE':
                        pass
                    case 'ELEMENTARY':
                        number_to_generate = random.randrange(0, 10)
                        for _ in range(0, number_to_generate):
                            classeswriter.writerow( fakeStudentRow(row[0], '4th Grade') )
                        number_to_generate = random.randrange(0, 10)
                        for _ in range(0, number_to_generate):
                            classeswriter.writerow(fakeStudentRow(row[0], '5th Grade'))
                        pass
                    case 'MIDDLE SCHOOL':
                        number_to_generate = random.randrange(0, 10)
                        for _ in range(0, number_to_generate):
                            classeswriter.writerow(fakeStudentRow(row[0], '6th Grade'))
                        number_to_generate = random.randrange(0, 10)
                        for _ in range(0, number_to_generate):
                            classeswriter.writerow(fakeStudentRow(row[0], '7th Grade'))
                        number_to_generate = random.randrange(0, 10)
                        for _ in range(0, number_to_generate):
                            classeswriter.writerow(fakeStudentRow(row[0], '8th Grade'))
                    case 'HIGH SCHOOL':
                        number_to_generate = random.randrange(0, 10)
                        for _ in range(0, number_to_generate):
                            classeswriter.writerow(fakeStudentRow(row[0], '9th Grade'))
                        number_to_generate = random.randrange(0, 10)
                        for _ in range(0, number_to_generate):
                            classeswriter.writerow(fakeStudentRow(row[0], '10th Grade'))
                        number_to_generate = random.randrange(0, 10)
                        for _ in range(0, number_to_generate):
                            classeswriter.writerow(fakeStudentRow(row[0], '11th Grade'))
                        for _ in range(0, number_to_generate):
                            classeswriter.writerow(fakeStudentRow(row[0], '11th Grade'))
                        pass
                    case _:
                        pass





