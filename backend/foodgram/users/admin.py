from django.contrib import admin

from .models import User


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('id', 'username', 'email', 'first_name', 'last_name',)
    list_filter = ('email', 'role', 'username',)
    search_fields = ('username', 'email',)
    empty_value_display = 'Введите данные'
