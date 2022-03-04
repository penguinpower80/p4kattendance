import csv
import logging

from attendance.forms.importfiles import FileType
from attendance.models import School, Classroom, Student


def handle_uploaded_file(type, file):
    reader = csv.DictReader( file )
    logging.warning(type)
    for row in reader:
        if type == FileType.SCHOOL:
            school = School()
            school.id = row['AGENCYID']
            school.name = row['NAME']
            school.type = row['TYPE']
            school.save()
        if type == FileType.STUDENT:
            try:
                classroom = Classroom.objects.filter(school_id__exact=row['SCHOOL ID'], name__exact=row['CLASSROOM'] ).get()
            except Classroom.DoesNotExist:
                classroom = Classroom()
                classroom.name=row['CLASSROOM']
                classroom.school_id=row['SCHOOL ID']
                classroom.save()

            student = Student()
            student.classroom = classroom
            student.first_name = row['FIRST']
            student.last_name = row['LAST']
            student.nde_id = row['NDE ID']
            student.dob = row['DOB']
            student.gender = row['GENDER']
            student.street = row['STREET']
            student.city = row['CITY']
            student.zip = row['STATE']
            student.email = row['EMAIL']
            student.phone = row['PHONE']
            student.notes = row['NOTE']
            student.save()


