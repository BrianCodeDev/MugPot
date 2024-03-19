# admin.py

from django.contrib import admin
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import Task
from .forms import SignUpForm
from .models import Task, Profile
from .forms import SignUpForm, ProfileForm

class ProfileInline(admin.StackedInline):
    model = Profile
    can_delete = False
    verbose_name_plural = 'Profile'
class UserAdmin(BaseUserAdmin):
    inlines = (ProfileInline,)
    add_form = SignUpForm
    fieldsets = (
        (None, {'fields': ('username', 'email',)}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email'),
        }),
    )
    list_display = ('username', 'email', 'is_staff')

    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)
        if not change:
            Profile.objects.create(user=obj)

# Unregister default UserAdmin
admin.site.unregister(User)

# Register custom UserAdmin
admin.site.register(User, UserAdmin)

# Register other models if needed
admin.site.register(Task)
# Register Profile model
admin.site.register(Profile)