from django.contrib import admin
from .models import User, IDCard

class UserAdmin(admin.ModelAdmin):
    list_display = ('name', 'email')
    search_fields = ('name', 'email')

class IDCardAdmin(admin.ModelAdmin):
    list_display = ('user', 'id_number', 'verified')
    list_filter = ('verified',)
    search_fields = ('user__name', 'id_number')

    def get_user_name(self, obj):
        return obj.user.name
    get_user_name.admin_order_field = 'user'  # Allows column to be sorted
    get_user_name.short_description = 'User Name'  # Renames column head

admin.site.register(User, UserAdmin)
admin.site.register(IDCard, IDCardAdmin)
