from django.urls import path

from . import views
app_name = 'attendance'

urlpatterns = [
          path('', views.home, name='home'),
          path('import', views.importfiles, name='import'),
          path('assignments', views.assignments, name='assignments'),
          path('assignments/<int:userid>', views.assign, name='assign'),
          path('meeting/<str:type>/<str:id>', views.meeting, name='meeting'),
          path('meeting/<int:id>', views.editmeeting, name='editmeeting'),
          path('ajax/markattendance/<int:meeting_id>/<str:student_id>', views.markattendance, name='markattendance'),
          path('ajax/meetinglist/<str:entity>/<str:entity_id>', views.meetinglist, name='meetinglist'),
          path('ajax/setmeetingdate/<int:meeting_id>', views.setmeetingdate, name='setmeetingdate')
]
