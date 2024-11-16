from django.contrib import admin

# Register your models here.
from .models import User


@admin.register(User)
class UserCustomAdmin(admin.ModelAdmin):
    model = User
    list_display = ('id', 'email', 'verified', 'is_staff', 'last_login', )
    search_fields = ('email', 'id', )
    ordering = ('id', )
