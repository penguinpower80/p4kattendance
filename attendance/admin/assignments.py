from django.contrib import admin

from attendance.models import Assignments


class AssignmentAdmin(admin.ModelAdmin):
    pass


admin.site.register(Assignments, AssignmentAdmin)
