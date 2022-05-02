"""
Register database models to Django admin panel.
"""
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Coach, Project, ProjectSuggestion, RequiredSkills, Skill, Student, Suggestion
from .forms import UserAdminChangeForm, UserAdminCreationForm

@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    """
    StudentAdmin; Just display first and last name on the change list page of the admin.
    """
    list_display = ('first_name', 'last_name',)

class CustomUserAdmin(UserAdmin):
    """
    ! This function only exists because of an issue that passwords would be saved in plaintext
    when creating new users in the admin panel !
    Here you define what fields are listed when
    changing a user, listing a user and creating a user.
    > We exclude the username because of form issues since we're using emails as pk.
    > Ordering needs to be changed because otherwise it tries to order on non-existant username.
    > form: the fields that change when changing a user.
    > add_form: the fields that are required when creating a user.
    > fieldsset: the visible fieldsets in the admin panel when changing a user.
    > add_fieldsets: the visible fieldsets in the admin panel when creating a user.
    """
    exclude = ('username',)
    ordering = ('email',)
    form = UserAdminChangeForm
    add_form = UserAdminCreationForm
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal info', {'fields': ('first_name', 'last_name', 'is_active')}),
        ('Permissions', {'fields': ('is_admin','is_staff')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email','password','first_name','last_name')}
        ),
        ('Permissions', {'fields': ('is_admin','is_staff')}),
    )

admin.site.register(Coach, CustomUserAdmin)
admin.site.register(Skill)
admin.site.register(Project)
admin.site.register(Suggestion)
admin.site.register(RequiredSkills)
admin.site.register(ProjectSuggestion)
