from django.urls import path

from . import views
app_name = 'attendance'

urlpatterns = [
          path('', views.home, name='home'),
          path('import', views.importfiles, name='import'),
          path('users', views.users, name='users'),
          path('adduser/<str:type>', views.adduser, name='adduser'),
          path('edituser/<int:id>', views.edituser, name='edituser'),
          path('deleteuser<int:id>', views.deleteuser, name='deleteuser'),
          path('assignments', views.assignments, name='assignments'),
          path('assignments/<int:userid>', views.assign, name='assign'),
          path('meeting/delete/<int:id>', views.deletemeeting, name='deletemeeting'),
          path('meeting/<int:id>', views.editmeeting, name='editmeeting'),
          path('meeting/<str:type>/<str:id>', views.meeting, name='meeting'),
          path('ajax/markattendance/<int:meeting_id>/<str:student_id>', views.markattendance, name='markattendance'),
          path('ajax/meetinglist/<str:entity>/<str:entity_id>', views.meetinglist, name='meetinglist'),
          path('ajax/note/delete/<int:id>', views.deletenote, name='deletenote'),
          path('ajax/noteslist/<str:entity>/<str:entity_id>', views.noteslist, name='noteslist'),
          path('ajax/setmeetingdate/<int:meeting_id>', views.setmeetingdate, name='setmeetingdate'),
          path('ajax/savenote/<str:entity>/<str:entity_id>', views.savenote, name='savenote'),
          path('ajax/updatenote/<int:note_id>', views.updatenote, name='updatenote'),
          path('profile', views.profile, name='profile'),
          path('reports', views.reports, name='reports'),
          path('reports/send/<str:report_type>', views.sendReport, name='sendreport'),
]
