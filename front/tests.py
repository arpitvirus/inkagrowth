from django.test import TestCase, override_settings

from .models import InternalLink, OutboundLink, SEOPageTemplate


@override_settings(ALLOWED_HOSTS=["testserver"], SECURE_SSL_REDIRECT=False)
class SEOPageTemplateTests(TestCase):
    def setUp(self):
        self.page = SEOPageTemplate.objects.create(
            service="Digital Marketing Services",
            city="Chandausi",
            state="Uttar Pradesh",
            primary_keyword="Digital Marketing Services in Chandausi",
            slug="digital-marketing-services-in-chandausi",
            meta_title="Digital Marketing Services in Chandausi | INKAGROWTH",
            meta_description=(
                "Digital Marketing Services in Chandausi helps local brands improve search visibility, leads, "
                "website trust, and measurable growth with INKAGROWTH."
            ),
        )
        internal_links = [
            ("SEO services", "/seo-services/"),
            ("website development", "/website-development/"),
            ("contact our growth team", "/contact/"),
            ("meet the INKAGROWTH team", "/team/"),
        ]
        for index, (title, url) in enumerate(internal_links):
            InternalLink.objects.update_or_create(
                url=url,
                defaults={"title": title, "category": "general"},
            )
            OutboundLink.objects.create(
                title=f"authority resource {index}",
                url=f"https://example.com/resource-{index}",
                category="general",
            )

    def test_valid_seo_page_renders_dynamic_links_and_metadata(self):
        response = self.client.get(f"/{self.page.slug}/")

        self.assertEqual(response.status_code, 200)
        html = response.content.decode()
        self.assertIn("<h1>Digital Marketing Services in Chandausi", html)
        self.assertIn("<link rel=\"canonical\"", html)
        self.assertIn("property=\"og:title\"", html)
        self.assertIn("BreadcrumbList", html)
        self.assertGreaterEqual(html.count('rel="noopener noreferrer"'), 4)
        self.assertGreaterEqual(html.count('class="inline-link"'), 8)

    def test_broken_internal_link_blocks_rendering(self):
        InternalLink.objects.all().delete()
        InternalLink.objects.create(
            title="broken local resource",
            url="/missing-local-page/",
            category="general",
        )

        response = self.client.get(f"/{self.page.slug}/")

        self.assertEqual(response.status_code, 422)
        self.assertIn("Broken internal links", response.content.decode())

    def test_invalid_seo_page_returns_validation_errors(self):
        self.page.meta_title = "Bad title"
        self.page.save(update_fields=["meta_title"])

        response = self.client.get(f"/{self.page.slug}/")

        self.assertEqual(response.status_code, 422)
        self.assertIn("SEO page validation failed", response.content.decode())
