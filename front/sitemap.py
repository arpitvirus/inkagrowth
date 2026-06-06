from django.contrib.sitemaps import Sitemap


class StaticSitemap(Sitemap):
    priority = 1.0
    changefreq = "monthly"

    def items(self):
        return ["home", "contact"]

    def location(self, item):
        return "/" if item == "home" else "/contact/"
