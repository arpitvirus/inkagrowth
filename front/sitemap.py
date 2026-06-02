from django.contrib.sitemaps import Sitemap
from .models import SEOPageTemplate

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
        return SEOPageTemplate.objects.filter(is_published=True)

    def location(self, obj):
        return f'/{obj.slug}/'
