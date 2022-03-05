import csv
import logging

from django.db import IntegrityError

from attendance.forms.importfiles import FileType
from attendance.models import School, Classroom, Student


def handle_uploaded_file(type, file):
    reader = csv.DictReader( file )
    result = {
        "status":"",
        "message":"",
        "rows":[]
    }

    if type == FileType.SCHOOL:
        for row in reader:
            try:
                school = School.objects.filter(id__exact=row['AGENCYID']).get()
                school.name = row['NAME']
                school.type = row['TYPE']
                school.save()
                row['STATUS']='UPDATED'
                result['rows'].append(row)
            except School.DoesNotExist:
                school = School()
                school.id = row['AGENCYID']
                school.name = row['NAME']
                school.type = row['TYPE']
                school.save()
                row['STATUS'] = 'ADDED'
                result['rows'].append(row)
            except KeyError:
                result['status'] = 'error'
                result['message'] = 'Invalid school file. Please check your format and try again.'
                return result
        result['status'] = 'success'
        result['message'] = 'The school file was imported succesfully'
        return result
    if type == FileType.STUDENT:
        for row in reader:
            try:
                classroom = Classroom.objects.filter(school_id__exact=row['SCHOOL ID'], name__exact=row['CLASSROOM'] ).get()
            except Classroom.DoesNotExist:
                classroom = Classroom()
                classroom.name=row['CLASSROOM']
                classroom.school_id=row['SCHOOL ID']
                try:
                    classroom.save()
                except IntegrityError:
                    row['STATUS'] = 'ERROR'
                    row['MESSAGE'] = 'NO SCHOOL LOADED'
                    result['rows'].append(row)
                    continue
            except KeyError:
                result['status'] = 'error'
                result['message'] = 'Invalid student file. Please check your format and try again.'
                return result
            try:
                student = Student.objects.filter(nde_id__exact=row['NDE ID']).get()
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
                row['STATUS'] = 'UPDATED'
                result['rows'].append(row)
            except Student.DoesNotExist:
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
                row['STATUS'] = 'ADDED'
                result['rows'].append(row)
            except KeyError:
                result['status'] = 'error'
                result['message'] = 'Invalid student file. Please check your format and try again.'
                return result
        result['status'] = 'success'
        result['message'] = 'The student file was imported succesfully'
        return result
    result['status'] = 'error'
    result['message'] = 'Unknown file type'
    return result