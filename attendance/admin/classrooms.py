from django.contrib import admin

from attendance.models import Classroom


class ClassroomsAdmin(admin.ModelAdmin):
    pass


admin.site.register(Classroom, ClassroomsAdmin)
