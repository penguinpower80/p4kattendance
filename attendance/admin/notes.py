from django.contrib import admin

from attendance.models import Notes


class NotesAdmin(admin.ModelAdmin):
    pass


admin.site.register(Notes, NotesAdmin)
