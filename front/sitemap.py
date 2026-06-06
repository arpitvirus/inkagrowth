from django.contrib.sitemaps import Sitemap


class StaticSitemap(Sitemap):
    priority = 1.0
    changefreq = "monthly"

    def items(self):
        return [
            "home",
            "about",
            "contact",
            "team",
            "privacy",
            "terms",
            "blog",
        ]

    def location(self, item):
        locations = {
            "home": "/",
            "about": "/about-inkagrowth/",
            "contact": "/contact/",
            "team": "/team/",
            "privacy": "/privacy-policy/",
            "terms": "/terms-and-conditions/",
            "blog": "/blog/",
        }
        return locations[item]
