from django.urls import path
from django.contrib.auth import views as auth_views
from . import views
app_name = 'attendance'

urlpatterns = [
          path('', views.home, name='home'),
          path('password_change/', auth_views.PasswordChangeView.as_view(template_name='registration/password_change.html'), name='password_change'),
          path('import', views.importfiles, name='import'),
          path('assignments', views.assignments, name='assignments'),
          path('assignments/<int:userid>', views.assign, name='assign'),
          path('meeting/<str:type>/<str:id>', views.meeting, name='meeting'),
          path('meeting/edit/<str:id>', views.editmeeting, name='editmeeting')
]
