from django.contrib.sitemaps import Sitemap
from .models import SEOPage

class StaticSitemap(Sitemap):
    priority = 1.0
    changefreq = "daily"

    def items(self):
        return ['home']

    def location(self, item):
        return '/'


class SEOPageSitemap(Sitemap):
    priority = 0.9
    changefreq = "daily"

    def items(self):
        return SEOPage.objects.all()

    def location(self, obj):
        return f'/{obj.slug}/'