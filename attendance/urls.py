from django.urls import path

from . import views
from .views.reports import ReportListView

app_name = 'attendance', ReportListView

urlpatterns = [
          path('', views.home, name='home'),
          path('import', views.importfiles, name='import'),
          path('assignments', views.assignments, name='assignments'),
          path('', ReportListView.as_view(), name='reports'),
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
]
