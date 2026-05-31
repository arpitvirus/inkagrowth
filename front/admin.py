from django.contrib import admin
from .models import SEOPage, contact

@admin.register(SEOPage)
class SEOPageAdmin(admin.ModelAdmin):
    list_display = (
        'city',
        'service',
        'slug',
        'meta_title'
    )

    search_fields = (
        'city',
        'service',
        'slug',
        'meta_title'
    )

    list_filter = (
        'city',
        'service'
    )

    prepopulated_fields = {
        'slug': ('service', 'city')
    }


@admin.register(contact)
class ContactAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'email',
        'mobile'
    )

    search_fields = (
        'name',
        'email',
        'mobile'
    )