from django.contrib import admin
from .models import (
    AuthorProfile,
    Category,
    FAQ,
    InternalLink,
    MediaFile,
    OutboundLink,
    Post,
    SEOAnalysisResult,
    SEOPage,
    SEOPageTemplate,
    Tag,
    contact,
)

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


class FAQInline(admin.TabularInline):
    model = FAQ
    extra = 1


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ("title", "slug", "status", "category", "author", "published_at", "seo_score", "readability_score")
    search_fields = ("title", "slug", "focus_keyphrase", "meta_title")
    list_filter = ("status", "category", "robots_index", "robots_follow")
    prepopulated_fields = {"slug": ("title",)}
    filter_horizontal = ("tags", "internal_links", "outbound_links")
    inlines = (FAQInline,)


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("name", "slug", "is_indexable")
    prepopulated_fields = {"slug": ("name",)}
    search_fields = ("name", "slug")


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ("name", "slug", "is_indexable")
    prepopulated_fields = {"slug": ("name",)}
    search_fields = ("name", "slug")


@admin.register(MediaFile)
class MediaFileAdmin(admin.ModelAdmin):
    list_display = ("title", "alt_text", "uploaded_by", "created_at")
    search_fields = ("title", "alt_text")


@admin.register(AuthorProfile)
class AuthorProfileAdmin(admin.ModelAdmin):
    list_display = ("display_name", "user")
    search_fields = ("display_name", "user__username", "user__email")


@admin.register(SEOAnalysisResult)
class SEOAnalysisResultAdmin(admin.ModelAdmin):
    list_display = ("post", "seo_score", "readability_score", "analyzed_at")
