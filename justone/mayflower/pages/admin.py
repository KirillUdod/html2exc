from pages.models import Page
from django.contrib import admin
from mce_filebrowser.admin import MCEFilebrowserAdmin


class PageAdmin(MCEFilebrowserAdmin):
    list_display = ['id', 'header', 'code']
    search_fields = ['header', 'code']

admin.site.register(Page, PageAdmin)