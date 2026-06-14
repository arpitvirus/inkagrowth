from django.contrib.sitemaps import Sitemap


class StaticSitemap(Sitemap):
    priority = 1.0
    changefreq = "monthly"

    def items(self):
        return [
            "home",
            "services",
            "results",
            "about",
            "clients",
            "contact",
            "about_inkagrowth",
            "team",
            "privacy",
            "terms",
            "blog",
            "digital_marketing_services",
            "seo_services",
            "social_media_marketing",
            "website_development",
            "google_ads_services",
            "lead_generation_services",
            "branding_services",
            "performance_marketing_services",
        ]

    def location(self, item):
        locations = {
            "home": "/",
            "services": "/services/",
            "results": "/results/",
            "about": "/about/",
            "clients": "/clients/",
            "contact": "/contact/",
            "about_inkagrowth": "/about-inkagrowth/",
            "team": "/team/",
            "privacy": "/privacy-policy/",
            "terms": "/terms-and-conditions/",
            "blog": "/blog/",
            "digital_marketing_services": "/digital-marketing-services/",
            "seo_services": "/seo-services/",
            "social_media_marketing": "/social-media-marketing/",
            "website_development": "/website-development/",
            "google_ads_services": "/google-ads-services/",
            "lead_generation_services": "/lead-generation-services/",
            "branding_services": "/branding-services/",
            "performance_marketing_services": "/performance-marketing-services/",
        }
        return locations[item]
