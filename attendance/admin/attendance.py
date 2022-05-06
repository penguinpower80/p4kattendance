from django.contrib import admin

from attendance.models import Attendance


class AttendanceAdmin(admin.ModelAdmin):
    pass


admin.site.register(Attendance, AttendanceAdmin)
