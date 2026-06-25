from django.contrib import admin

from .models import PortfolioProject, contact


@admin.register(contact)
class ContactAdmin(admin.ModelAdmin):
    list_display = ("name", "email", "mobile")
    search_fields = ("name", "email", "mobile", "message")


@admin.register(PortfolioProject)
class PortfolioProjectAdmin(admin.ModelAdmin):
    list_display = (
        "business_name",
        "business_category",
        "location",
        "service_type",
        "status",
        "is_featured",
        "created_at",
    )
    list_filter = ("service_type", "status", "location", "is_featured")
    search_fields = ("business_name", "business_category", "location", "focus_keyword")
    prepopulated_fields = {"slug": ("business_name",)}
    readonly_fields = ("created_at", "updated_at")
    fieldsets = (
        (
            "Basic Details",
            {
                "fields": (
                    "business_name",
                    "slug",
                    "business_category",
                    "location",
                    "short_description",
                    "cover_image",
                    "client_logo",
                    "status",
                    "is_featured",
                    "display_order",
                )
            },
        ),
        ("Services", {"fields": ("services_provided", "service_type")}),
        (
            "Case Study Content",
            {
                "fields": (
                    "client_overview",
                    "problem",
                    "strategy",
                    "work_done",
                    "keywords_targeted",
                    "result_summary",
                    "before_inkagrowth",
                    "after_inkagrowth",
                )
            },
        ),
        (
            "Result Metrics",
            {
                "fields": (
                    "keywords_targeted_count",
                    "search_visibility",
                    "profile_views",
                    "direction_requests",
                    "calls_received",
                    "leads_generated",
                    "campaigns_run",
                )
            },
        ),
        ("Links", {"fields": ("website_url", "instagram_url", "facebook_url", "google_maps_url")}),
        (
            "Testimonial",
            {
                "fields": (
                    "testimonial_text",
                    "testimonial_person_name",
                    "testimonial_person_designation",
                )
            },
        ),
        (
            "SEO Settings",
            {
                "fields": (
                    "meta_title",
                    "meta_description",
                    "focus_keyword",
                    "canonical_url",
                    "og_title",
                    "og_description",
                    "og_image",
                    "created_at",
                    "updated_at",
                )
            },
        ),
    )
