from django.contrib.sitemaps import Sitemap
from django.urls import reverse
from .models import SEOPage


class StaticViewSitemap(Sitemap):
    priority = 0.8
    changefreq = 'weekly'

    def items(self):
        return [
            'home',
            'about',
            'contact',
            'services',
        ]

    def location(self, item):
        return reverse(item)


class SEOPageSitemap(Sitemap):
    changefreq = "daily"
    priority = 0.9

    def items(self):
        return SEOPage.objects.all()

    def location(self, obj):
        return f'/{obj.slug}/'