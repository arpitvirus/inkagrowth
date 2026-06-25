from django.contrib.sitemaps import Sitemap

from .models import PortfolioProject
from .views import BLOG_POSTS, SERVICE_LANDING_PAGES


class CanonicalDomainSitemap(Sitemap):
    protocol = "https"
    domain = "www.inkagrowth.com"

    def get_domain(self, site=None):
        return self.domain


class StaticViewSitemap(CanonicalDomainSitemap):
    changefreq = "monthly"

    def items(self):
        items = [
            {"path": "/", "priority": 1.0},
            {"path": "/about/", "priority": 0.9},
            {"path": "/services/", "priority": 0.9},
            {"path": "/contact/", "priority": 0.9},
            {"path": "/results/", "priority": 0.8},
            {"path": "/clients/", "priority": 0.8},
            {"path": "/about-inkagrowth/", "priority": 0.8},
            {"path": "/team/", "priority": 0.8},
            {"path": "/privacy-policy/", "priority": 0.6},
            {"path": "/terms-and-conditions/", "priority": 0.6},
            {"path": "/blog/", "priority": 0.8},
        ]
        items.extend({"path": page["path"], "priority": 0.85} for page in SERVICE_LANDING_PAGES.values())
        items.extend({"path": f"/blog/{slug}/", "priority": 0.7} for slug in BLOG_POSTS)
        return items

    def location(self, item):
        return item["path"]

    def priority(self, item):
        return item["priority"]


class PortfolioListingSitemap(CanonicalDomainSitemap):
    changefreq = "weekly"
    priority = 0.8

    def items(self):
        return ["portfolio"]

    def location(self, item):
        return "/portfolio/"


class PortfolioSitemap(CanonicalDomainSitemap):
    changefreq = "monthly"
    priority = 0.7

    def items(self):
        return PortfolioProject.live()

    def lastmod(self, obj):
        return obj.updated_at

    def location(self, obj):
        return obj.get_absolute_url()


sitemaps = {
    "static": StaticViewSitemap,
    "portfolio-listing": PortfolioListingSitemap,
    "portfolio": PortfolioSitemap,
}
