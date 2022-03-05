from django.urls import path

from . import views
app_name = 'attendance'

urlpatterns = [
          path('', views.home, name='home'),
          path('import', views.importfiles, name='import'),
          path('widgettest', views.assigntest, name='assigntest')
]