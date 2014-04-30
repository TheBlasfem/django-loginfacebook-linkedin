from django.contrib import admin
from django.contrib.auth.models import Group
from django.contrib.auth.admin import UserAdmin

from hackusername.models import MyUser, Role, RoleUser, Permission, RolePermission
from hackusername.forms import UserChangeAdminForm, UserCreationAdminForm


class RoleUserInline(admin.TabularInline):
    model = RoleUser

class MyUserAdmin(UserAdmin):
    # The forms to add and change user instances
    form = UserChangeAdminForm
    add_form = UserCreationAdminForm

    # The fields to be used in displaying the User model.
    # These override the definitions on the base UserAdmin
    # that reference specific fields on auth.User.
    list_display = ('email', 'date_of_birth', 'is_admin',
                    'name', 'commercial_name',
                    'business_name', 'ruc', 'address',
                    'phone', 'web', 'description'
                    )

    list_filter = ('is_admin',)
    fieldsets = (
        (None, {'fields': ('email', 'password', 'password1', 'password2')}),
        ('Personal info', {'fields': ('date_of_birth',
         'name',
         'commercial_name',
         'business_name',
         'ruc',
         'address',
         'phone',
         'web',
         'description',
         'facebook_id',
         'linkedin_id')}),
        ('Permissions', {'fields': ('is_admin', 'is_staff', 'groups', 'user_permissions')}),
    )
    # add_fieldsets is not a standard ModelAdmin attribute. UserAdmin
    # overrides get_fieldsets to use this attribute when creating a user.
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'name',
                       'password1', 'password2'
                      )}
         ),
    )
    search_fields = ('email',)
    ordering = ('email',)
    filter_horizontal = ()

    inlines = [
        RoleUserInline,
    ]


class RolePermissionInline(admin.TabularInline):
    model = RolePermission


class RolAdmin(admin.ModelAdmin):
    inlines = [
        RolePermissionInline
    ]

# Now register the new UserAdmin...
admin.site.register(MyUser, MyUserAdmin)
# ... and, since we're not using Django's built-in permissions,
# unregister the Group model from admin.
#admin.site.unregister(Group)
admin.site.register(Role, RolAdmin)
#admin.site.register(Rol)
admin.site.register(Permission)
#admin.site.register(RolUsuario)
#admin.site.register(RolPermiso)