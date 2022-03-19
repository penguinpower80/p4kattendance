from collections import OrderedDict

from django.shortcuts import redirect
from django.urls import reverse

from attendance.models import Assignments, AssignmentTypes, School, Student, Classroom


def is_mentor(user):
    return user.groups.filter(name='Mentors').exists()

def is_facilitator(user):
    return user.groups.filter(name='Facilitators').exists()

def isAssigned(user, id, type):
    return Assignments.objects.filter(user=user).filter(tid=id).filter(type=type).count() > 0

'''
Build the widget hierarchy for a given set of assignments
School
  -> Class Room
     -> Student
For any given classroom, we need a school
For any given student, we need a classroom and a school
'''
def buildAssignmentHierarchy( query_set ):
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
                hierarchy[ student.classroom.school_id ] = {
                     'name': student.classroom.school.name,
                     'classrooms': {
                         student.classroom.id : {
                             'name': student.classroom.name,
                             'students': [
                                 student
                             ]
                         }
                     }
                }
            else: #ok, so school exists
                # does the classroom exist, if yes:
                if student.classroom.id not in hierarchy[ student.classroom.school_id ]['classrooms']:
                    hierarchy[student.classroom.school_id]['classrooms'][ student.classroom.id ] = {
                        'name': student.classroom.name,
                        'students': [
                            student
                        ]
                    }
                else: # school and classroom exist, so just add the student
                    hierarchy[student.classroom.school_id]['classrooms'][student.classroom.id]['students'].append(student)

    # For each of the needed classrooms, make sure the "assigned" attribute is True, even if added for a student
    if len(needed_classrooms) > 0:
        classroom_collection = Classroom.objects.filter(pk__in=needed_classrooms)
        for classroom in classroom_collection:
            if classroom.school_id not in hierarchy:
                hierarchy[ classroom.school_id ] = {
                     'name': classroom.school.name,
                     'classrooms': {
                         classroom.id : {
                             'name': classroom.name,
                             'assigned': True
                         }
                     }
                }
            else: #ok, so school exists
                # does the classroom exist, if yes:
                if classroom.id not in hierarchy[ classroom.school_id ]['classrooms']:
                    hierarchy[classroom.school_id]['classrooms'][ classroom.id ] = {
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
            #if school hasn't been added previously
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
        sorted_hierarchy[ k ] = hierarchy[k]
    return sorted_hierarchy


'''
Get the assignments for a given user. If type is set, only get that type of assignment (school, classroom, student). If 
hierarchical is True, then generate a hierarchical list, including parent items that may NOT have been assigned but are
needed for display purposes
'''
def assignmentsFor(user, type=None, hierarchical = False):
    if ( type ):
        results = Assignments.objects.filter(user=user).filter(type=type).all()
    else:
        results = Assignments.objects.filter(user=user).all()
    if hierarchical:
        return buildAssignmentHierarchy(results)
    else:
        return results

def getRedirectWithParam(message, location='attendance:home'):
    base_url = reverse(location)
    url = '{}?msg={}'.format(base_url, message)
    return redirect(url)