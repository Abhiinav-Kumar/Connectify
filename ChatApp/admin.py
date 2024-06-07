from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from ChatApp.models import UserDB,Room,Message


class UserDBAdmin(UserAdmin):
    list_display = ('email', 'username', 'date_joined', 'last_login', 'is_admin','is_staff' 'is_active')
    search_fields = ('email', 'username')
    readonly_fields = ('id','date_joined', 'last_login')

    filter_horizontal = ()
    list_filter = ()
    fieldsets = ()

    # add_fieldsets = (
    #     (None, {
    #         'classes': ('wide',),
    #         'fields': ('email', 'username', 'password1', 'password2', 'is_active', 'is_admin')}
    #     ),
    # )

# Register your models here.
admin.site.register(UserDB)
admin.site.register(Room)
admin.site.register(Message)

