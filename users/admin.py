from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.core.exceptions import ValidationError
from django.contrib.auth.forms import ReadOnlyPasswordHashField
# Register your models here.

class CustomUserCreationForm(UserCreationForm):

    class Meta:
        model = User
        fields = ('email',)


class CustomUserChangeForm(UserChangeForm):

    class Meta:
        model = User
        fields = ('email',)




class UserAdminConfig(UserAdmin):
     #model=User
    # form = UserChangeForm
    # add_form = UserCreationForm
     ordering=('-created',)
     list_display=("email","user_name","full_name")
     fieldsets=(
         (None,{
             "fields":("email","user_name","full_name","password","is_active","is_superuser")
         }
         ),
         ('Permissions', {'fields': ('is_staff', 'groups', 'user_permissions')})
     ,)
     add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'user_name', 'full_name', 'password1', 'password2', 'is_active', 'is_staff')}
         ),
         ('Permissions', {'fields': ('is_staff', 'groups', 'user_permissions')})
    )

admin.site.register(User,UserAdminConfig)