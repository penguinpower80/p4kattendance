from django.contrib import admin

from attendance.models import Student


class StudentsAdmin(admin.ModelAdmin):
    pass

admin.site.register(Student, StudentsAdmin)