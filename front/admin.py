from django.contrib import admin

from .models import contact


@admin.register(contact)
class ContactAdmin(admin.ModelAdmin):
    list_display = ("name", "email", "mobile")
    search_fields = ("name", "email", "mobile", "message")
