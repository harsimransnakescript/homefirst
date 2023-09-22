from django.contrib import admin
from . models import User, Otp, AllowedDomain, UserProfile
from .forms import UserCreationForm
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin



class UserAdmin(BaseUserAdmin):
    # The forms to add and change user instances
    
    add_form = UserCreationForm

    # The fields to be used in displaying the User model.
    # These override the definitions on the base UserAdmin
    # that reference specific fields on auth.User.
    list_display = ('username1','email', 'phone','first_name','login_otp','is_admin',"is_active")
    list_filter = ('is_admin',)
    fieldsets = (
        (None, {'fields': ('email','phone')}),
        ('Personal info', {'fields': ('first_name','last_name', 'username1','login_otp')}),
        ('Permissions', {'fields': ('is_admin',"is_active","is_manager","is_patient")}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'first_name',),
        }),
    )
    search_fields = ('email','phone')
    ordering = ('email','phone')
    filter_horizontal = ()

admin.site.register(User,UserAdmin)
admin.site.register(Otp)
admin.site.register(AllowedDomain)
admin.site.register(UserProfile)