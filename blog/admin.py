from django.contrib import admin

from blog.models import Blog


@admin.register(Blog)
class BlogAdmin(admin.ModelAdmin):
    list_display = ('topic', 'content', 'preview', 'views_count', 'public_date',)
