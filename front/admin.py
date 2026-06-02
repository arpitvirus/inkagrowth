from django.contrib import admin
from .models import InternalLink, OutboundLink, SEOPage, SEOPageTemplate, contact

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


@admin.register(SEOPageTemplate)
class SEOPageTemplateAdmin(admin.ModelAdmin):
    list_display = (
        'service',
        'city',
        'state',
        'primary_keyword',
        'slug',
        'is_published',
    )

    search_fields = (
        'service',
        'city',
        'state',
        'primary_keyword',
        'slug',
        'meta_title',
    )

    list_filter = (
        'state',
        'service',
        'is_published',
    )

    prepopulated_fields = {
        'slug': ('service', 'city')
    }


@admin.register(InternalLink)
class InternalLinkAdmin(admin.ModelAdmin):
    list_display = ('title', 'url', 'category')
    search_fields = ('title', 'url', 'category')
    list_filter = ('category',)


@admin.register(OutboundLink)
class OutboundLinkAdmin(admin.ModelAdmin):
    list_display = ('title', 'url', 'category')
    search_fields = ('title', 'url', 'category')
    list_filter = ('category',)
