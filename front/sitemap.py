from django.contrib.sitemaps import Sitemap
from .models import SEOPage


class SEOPageSitemap(Sitemap):
    changefreq = "daily"
    priority = 0.9

    def items(self):
        return SEOPage.objects.all()

    def location(self, obj):
        return f'/{obj.slug}/'