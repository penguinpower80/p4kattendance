from django.urls import path

from . import views
app_name = 'attendance'

urlpatterns = [
          path('', views.home, name='home'),
          path('import', views.importfiles, name='import'),
          path('assignments', views.assignments, name='assignments'),
          path('assignments/<int:userid>', views.assign, name='assign'),
          path('meeting/<str:type>/<str:id>', views.meeting, name='meeting'),
          path('meeting/edit/<str:id>', views.editmeeting, name='editmeeting')
]
