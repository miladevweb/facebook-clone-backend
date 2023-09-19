from django.contrib import admin
from .models import Comment

class CommentAdmin(admin.ModelAdmin):
    ordering = ('-id',)

admin.site.register(Comment, CommentAdmin)