import logging
from collections import OrderedDict
from itertools import chain

from django.db.models import Q
from django.shortcuts import redirect
from django.urls import reverse

from attendance.models import Assignments, AssignmentTypes, School, Student, Classroom, Meeting

def format_time(time):
    try:
        time_format = '%m/%d/%Y %-I:%M %P'
        formatted = time.strftime(time_format)
    except ValueError:
        # Windows:
        time_format = '%m/%d/%Y %#I:%M %p'
        formatted = time.strftime(time_format)

    return formatted

def is_mentor(user):
    return user.groups.filter(name='Mentors').exists()


def is_facilitator(user):
    return user.groups.filter(name='Facilitators').exists()


def isAssigned(user, id, type):
    return Assignments.objects.filter(user=user).filter(tid=id).filter(type=type).count() > 0


def buildAssignmentHierarchy(query_set):
    '''
    Build the widget hierarchy for a given set of assignments
    School
      -> Class Room
         -> Student
    For any given classroom, we need a school
    For any given student, we need a classroom and a school
    '''
    hierarchy = {}
    needed_schools = []
    needed_students = []
    needed_classrooms = []
    # Step 1: Collect all assignment IDs based on type so we can do 3 queries instead of # of assignements queries
    for x in query_set:
        if x.type == AssignmentTypes.STUDENT:
            needed_students.append(x.tid)
        if x.type == AssignmentTypes.CLASSROOM:
            needed_classrooms.append(x.tid)
        if x.type == AssignmentTypes.SCHOOL:
            needed_schools.append(x.tid)
    if len(needed_students) > 0:
        student_collection = Student.objects.filter(pk__in=needed_students)
        for student in student_collection:
            if student.classroom.school_id not in hierarchy:
                hierarchy[student.classroom.school_id] = {
                    'name': student.classroom.school.name,
                    'classrooms': {
                        student.classroom.id: {
                            'name': student.classroom.name,
                            'students': [
                                student
                            ]
                        }
                    }
                }
            else:  # ok, so school exists
                # does the classroom exist, if yes:
                if student.classroom.id not in hierarchy[student.classroom.school_id]['classrooms']:
                    hierarchy[student.classroom.school_id]['classrooms'][student.classroom.id] = {
                        'name': student.classroom.name,
                        'students': [
                            student
                        ]
                    }
                else:  # school and classroom exist, so just add the student
                    hierarchy[student.classroom.school_id]['classrooms'][student.classroom.id]['students'].append(student)

    # For each of the needed classrooms, make sure the "assigned" attribute is True, even if added for a student
    if len(needed_classrooms) > 0:
        classroom_collection = Classroom.objects.filter(pk__in=needed_classrooms)
        for classroom in classroom_collection:
            if classroom.school_id not in hierarchy:
                hierarchy[classroom.school_id] = {
                    'name': classroom.school.name,
                    'classrooms': {
                        classroom.id: {
                            'name': classroom.name,
                            'assigned': True
                        }
                    }
                }
            else:  # ok, so school exists
                # does the classroom exist, if yes:
                if classroom.id not in hierarchy[classroom.school_id]['classrooms']:
                    hierarchy[classroom.school_id]['classrooms'][classroom.id] = {
                        'name': classroom.name,
                        'assigned': True
                    }
                else:
                    hierarchy[classroom.school_id]['classrooms'][classroom.id]['assigned'] = True

    # For each of the needed schools, make sure the "assigned" attribute is True, even if added for a student
    # may need to just get rid of this for mentors??
    if len(needed_schools) > 0:
        school_collection = School.objects.filter(pk__in=needed_schools)
        for school in school_collection:
            # if school hasn't been added previously
            if school.id not in hierarchy:
                hierarchy[school.id] = {
                    'name': school.name,
                    'assigned': True
                }
            else:
                hierarchy[school.id]['assigned'] = True

    keys = hierarchy.keys()
    sorth = sorted(keys, key=lambda x: hierarchy[x]['name'])
    sorted_hierarchy = OrderedDict()
    for k in sorth:
        sorted_hierarchy[k] = hierarchy[k]
    return sorted_hierarchy


def assignmentsFor(user, entity=None, hierarchical=False):
    '''
    Get the assignments for a given user. If type is set, only get that type of assignment (school, classroom, student). If
    hierarchical is True, then generate a hierarchical list, including parent items that may NOT have been assigned but are
    needed for display purposes
    '''
    if (entity):
        results = Assignments.objects.filter(user=user).filter(type=entity).all()
    else:
        results = Assignments.objects.filter(user=user).all()
    if hierarchical:
        return buildAssignmentHierarchy(results)
    else:
        return results


def meetingsFor(user, entity=None, entity_id=None, includeStudents=False):
    '''
    Retrieve all meetings for a given user, restricted to their assignments
    Based on: https://stackoverflow.com/questions/46278166/django-filter-to-check-if-both-multiple-fields-are-in-list
    '''
    assignments = assignmentsFor(user)
    # no assignments = no meetings
    if (len(assignments) == 0):
        return None

    assignment_filter = None
    assigned_students = []
    assigned_classrooms = []
    for a in assignments:
        if a.type == AssignmentTypes.CLASSROOM:
            assigned_classrooms.append(a.tid)
        if a.type == AssignmentTypes.STUDENT:
            assigned_students.append(a.tid)
    meetings = Meeting.objects.filter(user=user).filter(type=entity).order_by('-date')

    # this is for a specific student
    if entity == AssignmentTypes.STUDENT and entity_id is not None:
        return list(chain, meetings.filter(tid=entity_id).filter(tid__in=assigned_students)).values('date', 'id', 'tid', 'type')

    if entity == AssignmentTypes.CLASSROOM and entity_id is not None:
        if not includeStudents:
            return list(chain(meetings.filter(tid=entity_id).filter(tid__in=assigned_classrooms))).values('date', 'id', 'tid', 'type')
        else:
            meetings = meetings.filter(tid=entity_id).filter(tid__in=assigned_classrooms).values('date', 'id', 'tid', 'type')
            student_meetings = Meeting.objects.filter(user=user).filter(type=AssignmentTypes.STUDENT).filter(tid__in=assigned_students).values('date', 'id', 'tid', 'type')
            return list(chain(meetings, student_meetings))

    return None


def getRedirectWithParam(message, location='attendance:home', kwargs=None):
    '''
    Utility function to add a message to a url location and send back a redirect
    '''
    base_url = reverse(location, kwargs=kwargs)
    url = '{}?msg={}'.format(base_url, message)
    return redirect(url)

def userAssignedToStudent(user, student_id):
    '''
    Returns true if there is an entry in assignments linking this user with this student (either directly or through a class room or school)
    '''
    # was there a direct assignement?
    if Assignments.objects.filter(user=user).count() > 0:
        return True

    # let's see if they are assigned via a classroom
    try:
        student = Student.objects.get(pk=student_id)
    except Student.DoesNotExist:
        return False

    if Assignments.objects.filter(user=user).filter(type=AssignmentTypes.CLASSROOM).filter(tid=student.classroom_id).count() > 0:
        return True

    # let's see about through a school
    if Assignments.objects.filter(user=user).filter(type=AssignmentTypes.SCHOOL).filter(tid=student.classroom.school_id).count() > 0:
        return True
    # nope
    return False
