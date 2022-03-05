import logging
import os
from io import TextIOWrapper
from unittest import TestCase

import django.test
from django.core.files.uploadedfile import SimpleUploadedFile

from attendance.forms.importfiles import ImportFileForm
from attendance.models import Student, Classroom, School
from attendance.utility import handle_uploaded_file


class FileImportTestCase(django.test.TestCase):

    def test_file_required(self):
        form = ImportFileForm(data={"type": "student"})
        self.assertIsNotNone(
            form.errors['file']
        )

    def test_good_school_import(self):
        good_schools_file = 'attendance/tests/samples/schools.csv'
        if not os.path.exists(good_schools_file):
            raise AssertionError("File does not exist: {}".format(good_schools_file))

        with open(good_schools_file, 'rb') as infile:
            _file = SimpleUploadedFile(good_schools_file, infile.read())
            result = handle_uploaded_file('school', TextIOWrapper(_file.file) )
            self.assertIs(result['status'], 'success')

        count = School.objects.all().count()
        self.assertEqual(count, 82)

    def test_bad_school_import(self):
        bad_schools_file = 'attendance/tests/samples/students.csv'
        if not os.path.exists(bad_schools_file):
            raise AssertionError("File does not exist: {}".format(bad_schools_file))

        with open(bad_schools_file, 'rb') as infile:
            _file = SimpleUploadedFile(bad_schools_file, infile.read())
            result = handle_uploaded_file('school', TextIOWrapper(_file.file) )
            self.assertIs(result['status'], 'error')

        count = Student.objects.all().count()
        self.assertIs(count, 0)

    def test_good_student_import(self):
        with open('attendance/tests/samples/schools.csv', 'rb') as infile:
            _file = SimpleUploadedFile('attendance/tests/samples/schools.csv', infile.read())
            result = handle_uploaded_file('school', TextIOWrapper(_file.file) )

        good_student_file = 'attendance/tests/samples/students.csv'
        if not os.path.exists(good_student_file):
            raise AssertionError("File does not exist: {}".format(good_student_file))

        with open(good_student_file, 'rb') as infile:
            _file = SimpleUploadedFile(good_student_file, infile.read())
            result = handle_uploaded_file('student', TextIOWrapper(_file.file) )

            self.assertIs(result['status'], 'success')


        count = Student.objects.all().count()
        self.assertEqual(count, 445)

        count = Classroom.objects.all().count()
        self.assertEqual(count, 82)

    def test_bad_student_import(self):
        bad_student_file = 'attendance/tests/samples/schools.csv'
        if not os.path.exists(bad_student_file):
            raise AssertionError("File does not exist: {}".format(bad_student_file))

        with open(bad_student_file, 'rb') as infile:
            _file = SimpleUploadedFile(bad_student_file, infile.read())
            result = handle_uploaded_file('student', TextIOWrapper(_file.file) )
            self.assertIs(result['status'], 'error')
        count = Student.objects.all().count()
        self.assertIs( count, 0)


