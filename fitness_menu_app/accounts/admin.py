from django.contrib import admin
from django.contrib.auth import admin as auth_admin, get_user_model
# from django.contrib.auth.models import User

from fitness_menu_app.accounts.forms import CreateUserForm, FitnessMenuChangeForm

UserModel = get_user_model()


@admin.register(UserModel)
class AppUserAdmin(auth_admin.UserAdmin):
    model = UserModel
    add_form = CreateUserForm
    form = FitnessMenuChangeForm

    list_display = ('pk', 'username', 'is_staff', 'is_superuser')
    search_fields = ('username',)
    ordering = ('pk',)

    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Personal info', {'fields': ('first_name', 'last_name',)}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )

    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": ("username", "password1", "password2"),
            },
        ),
    )
