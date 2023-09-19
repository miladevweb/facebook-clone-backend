from django.contrib import admin
from .models import Post

class PostAdmin(admin.ModelAdmin):
    ordering = ('-id',)

admin.site.register(Post, PostAdmin)