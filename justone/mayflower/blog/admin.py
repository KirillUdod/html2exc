from django.contrib import admin

from blog.models import BlogMainPage, BlogItem, BlogTag
from mayflower.admin import SingleObjectAdmin, RedactorAdmin


class BlogImageInline(admin.TabularInline):
    max_num = 9


class BlogItemAdmin(RedactorAdmin):
    list_display = ['title', 'create_date']
    # inlines = [BlogImageInline]


admin.site.register(BlogMainPage, SingleObjectAdmin)
admin.site.register(BlogItem, BlogItemAdmin)
admin.site.register(BlogTag)