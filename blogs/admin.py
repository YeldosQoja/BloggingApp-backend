from django.contrib import admin
from .models import Blog, Comment

class CommentInline(admin.TabularInline):
    model = Comment
    extra = 3

class BlogAdmin(admin.ModelAdmin):
    fieldsets = [
        ("Blog Content", { "fields": ["title", "content"] }),
        ("Metadata", { "fields": ["num_likes", "tagline"] }),
        ("Date", { "fields": ["created_at"] })
    ]
    search_fields = ["title"]
    list_filter = ["num_likes", "created_at"]
    list_display = ["title", "num_likes", "created_at"]
    inlines = [CommentInline]

# Register your models here.
admin.register(Blog, BlogAdmin)