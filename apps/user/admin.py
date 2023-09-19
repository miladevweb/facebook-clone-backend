from django.contrib import admin
from .models import User

class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'id', )
    ordering = ('id',)

admin.site.register(User, UserAdmin)