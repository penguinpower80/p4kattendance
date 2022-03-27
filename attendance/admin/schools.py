from django.contrib import admin

from attendance.models import School


class SchoolsAdmin(admin.ModelAdmin):
    pass

admin.site.register(School, SchoolsAdmin)