from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User

from users.forms import UserRegisterForm
from users.models import CustomUser
from users.models import Billet

User = get_user_model()


class CustomUserAdmin(UserAdmin, admin.ModelAdmin):
    model = User
    readonly_fields = ('created_at', 'billet', 'many', 'data_joined', 'number')
    list_display_links = ['email']
    search_fields = ('email', 'username', 'is_active')
    ordering = ('email',)
    list_display = ('email', 'is_staff', 'is_active', 'is_superuser')
    list_filter = ('email', 'is_staff', 'is_active', 'is_superuser')
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        (('Personal info'),
         {'fields': (
         'first_name', 'last_name', 'email', 'phone', 'many', 'billet', 'number', 'created_at', 'data_joined')}),
        (('Permissions'), {
            'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions'),
        }),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2', 'is_staff', 'is_active', 'created_at')}
         ),
    )

    def get_inline_instances(self, request, obj=None):
        if not obj:
            return list()
        return super(CustomUserAdmin, self).get_inline_instances(request, obj)


admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(Billet)