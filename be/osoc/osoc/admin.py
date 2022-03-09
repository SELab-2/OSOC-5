from django.contrib import admin

from osoc.osoc.models import Student


@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name',)
