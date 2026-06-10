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
            "team",
            "privacy",
            "terms",
            "blog",
        ]

    def location(self, item):
        locations = {
            "home": "/",
            "services": "/services/",
            "results": "/results/",
            "about": "/about/",
            "clients": "/clients/",
            "contact": "/contact/",
            "team": "/team/",
            "privacy": "/privacy-policy/",
            "terms": "/terms-and-conditions/",
            "blog": "/blog/",
        }
        return locations[item]
