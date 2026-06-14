from django.test import TestCase, override_settings
from urllib.parse import urlparse
from urllib.robotparser import RobotFileParser
from xml.etree import ElementTree

from .models import contact
from .views import BLOG_POSTS, SERVICE_LANDING_PAGES


@override_settings(ALLOWED_HOSTS=["testserver"], SECURE_SSL_REDIRECT=False)
class FrontPageTests(TestCase):
    def test_homepage_renders(self):
        response = self.client.get("/")

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "INKAGROWTH Digital Marketing Agency")
        self.assertContains(response, "Official Digital Marketing Agency in Chandausi")
        self.assertContains(response, "BreadcrumbList")
        self.assertContains(response, "LocalBusiness")
        self.assertContains(response, "Organization")

    def test_contact_page_renders(self):
        response = self.client.get("/contact/")

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Contact INKAGROWTH")

    def test_homepage_contact_form_saves_contact(self):
        response = self.client.post(
            "/",
            {
                "name": "Test User",
                "email": "test@example.com",
                "mobile": "9999999999",
                "message": "Please contact me.",
            },
        )

        self.assertEqual(response.status_code, 302)
        self.assertEqual(contact.objects.count(), 1)

    def test_sitemap_and_robots_render(self):
        sitemap = self.client.get("/sitemap.xml")
        robots = self.client.get("/robots.txt")

        self.assertEqual(sitemap.status_code, 200)
        self.assertIn("/contact/", sitemap.content.decode())
        self.assertIn("/about-inkagrowth/", sitemap.content.decode())
        self.assertIn("/blog/who-is-inkagrowth/", sitemap.content.decode())
        self.assertEqual(robots.status_code, 200)
        self.assertEqual(
            robots.content.decode().strip(),
            "\n".join(
                [
                    "User-agent: *",
                    "Allow: /",
                    "",
                    "Disallow: /admin/",
                    "Disallow: /crm/",
                    "Disallow: /login/",
                    "Disallow: /dashboard/",
                    "",
                    "Sitemap: https://inkagrowth.com/sitemap.xml",
                ]
            ),
        )

    def test_sitemap_only_lists_crawlable_public_pages(self):
        sitemap = self.client.get("/sitemap.xml")
        robots = self.client.get("/robots.txt")

        self.assertEqual(sitemap.status_code, 200)
        self.assertEqual(robots.status_code, 200)

        parser = RobotFileParser()
        parser.parse(robots.content.decode().splitlines())

        root = ElementTree.fromstring(sitemap.content)
        namespace = {"sm": "http://www.sitemaps.org/schemas/sitemap/0.9"}
        locs = [loc.text for loc in root.findall(".//sm:loc", namespace)]
        paths = [urlparse(loc).path for loc in locs]

        self.assertIn("https://www.inkagrowth.com/", locs)
        self.assertIn("https://www.inkagrowth.com/contact/", locs)
        self.assertIn("https://www.inkagrowth.com/services/", locs)
        self.assertIn("https://www.inkagrowth.com/blog/", locs)

        for page in SERVICE_LANDING_PAGES.values():
            self.assertIn(f"https://www.inkagrowth.com{page['path']}", locs)

        for slug in BLOG_POSTS:
            self.assertIn(f"https://www.inkagrowth.com/blog/{slug}/", locs)

        for blocked_prefix in ["/admin/", "/crm/", "/login/", "/dashboard/"]:
            self.assertFalse(
                any(path.startswith(blocked_prefix) for path in paths),
                f"{blocked_prefix} should not be in sitemap.xml",
            )

        for loc in locs:
            self.assertTrue(parser.can_fetch("*", loc), f"{loc} is blocked by robots.txt")

    def test_public_sitemap_pages_are_indexable(self):
        sitemap = self.client.get("/sitemap.xml")
        root = ElementTree.fromstring(sitemap.content)
        namespace = {"sm": "http://www.sitemaps.org/schemas/sitemap/0.9"}
        paths = [urlparse(loc.text).path for loc in root.findall(".//sm:loc", namespace)]

        for path in paths:
            response = self.client.get(path)

            self.assertEqual(response.status_code, 200, path)
            self.assertNotEqual(response.headers.get("X-Robots-Tag"), "noindex", path)
            self.assertNotContains(response, "noindex", status_code=200)
            self.assertContains(
                response,
                '<meta name="robots" content="index, follow">',
                html=True,
            )

    def test_authority_pages_render(self):
        for path in [
            "/about-inkagrowth/",
            "/team/",
            "/privacy-policy/",
            "/terms-and-conditions/",
        ]:
            response = self.client.get(path)
            self.assertEqual(response.status_code, 200)
            self.assertContains(response, "INKAGROWTH")
            self.assertContains(response, "BreadcrumbList")

    def test_service_landing_pages_render(self):
        for page in SERVICE_LANDING_PAGES.values():
            response = self.client.get(page["path"])

            self.assertEqual(response.status_code, 200)
            self.assertContains(response, page["heading"])
            self.assertContains(response, page["description"])
            self.assertContains(response, '<meta name="robots" content="index, follow">', html=True)
            self.assertContains(response, f'<link rel="canonical" href="https://www.inkagrowth.com{page["path"]}">', html=True)

    def test_branded_blog_posts_render(self):
        for path in [
            "/blog/who-is-inkagrowth/",
            "/blog/why-businesses-choose-inkagrowth/",
            "/blog/inkagrowth-digital-marketing-services/",
            "/blog/inkagrowth-success-stories/",
            "/blog/inkagrowth-social-media-marketing-process/",
        ]:
            response = self.client.get(path)
            self.assertEqual(response.status_code, 200)
            self.assertContains(response, "INKAGROWTH")
            self.assertContains(response, "INKAGROWTH homepage")
