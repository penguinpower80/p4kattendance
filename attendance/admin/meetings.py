from django.contrib import admin

from attendance.models import Meeting


class MeetingsAdmin(admin.ModelAdmin):
    pass


admin.site.register(Meeting, MeetingsAdmin)
