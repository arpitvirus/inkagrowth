from django.contrib.auth import get_user_model
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase, override_settings
from django.utils import timezone

from .models import Category, InternalLink, MediaFile, OutboundLink, Post, SEOPageTemplate


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


@override_settings(ALLOWED_HOSTS=["testserver"], SECURE_SSL_REDIRECT=False)
class PublishingSystemTests(TestCase):
    def setUp(self):
        user_model = get_user_model()
        self.staff = user_model.objects.create_user("editor", "editor@example.com", "pass", is_staff=True)
        self.category = Category.objects.create(name="Digital Marketing", slug="digital-marketing")
        self.media = MediaFile.objects.create(
            title="Featured",
            file=SimpleUploadedFile("featured.jpg", b"tiny-image", content_type="image/jpeg"),
            alt_text="Digital Marketing in Chandausi",
            uploaded_by=self.staff,
        )
        for index, url in enumerate(["/seo-services/", "/website-development/", "/contact/", "/team/"]):
            InternalLink.objects.update_or_create(
                url=url,
                defaults={"title": f"internal resource {index}", "category": "general"},
            )
            OutboundLink.objects.update_or_create(
                url=f"https://example.org/resource-{index}",
                defaults={"title": f"outbound resource {index}", "category": "general"},
            )
        paragraphs = " ".join(
            [
                "Digital Marketing in Chandausi helps local businesses grow online with clear strategy, useful content, and better conversion tracking.",
                "Additionally, INKAGROWTH explains each step in simple language so owners can make confident decisions.",
                "Furthermore, the campaign connects SEO, website development, analytics, branding, and lead generation.",
            ]
            * 45
        )
        self.post = Post.objects.create(
            title="Digital Marketing in Chandausi",
            slug="digital-marketing-in-chandausi",
            focus_keyphrase="Digital Marketing in Chandausi",
            meta_title="Digital Marketing in Chandausi | INKAGROWTH Agency",
            meta_description="Digital Marketing in Chandausi helps local businesses grow with SEO, Meta Ads, branding, lead generation, and websites by INKAGROWTH.",
            excerpt="Digital marketing guide for Chandausi businesses.",
            content=f"<h2>Why Digital Marketing in Chandausi Matters</h2><p>{paragraphs}</p><h2>Benefits</h2><h3>Strategy</h3><h3>Getting Started</h3>",
            featured_image=self.media,
            featured_image_alt="Digital Marketing in Chandausi",
            category=self.category,
            author=self.staff,
            status=Post.STATUS_PUBLISHED,
            published_at=timezone.now(),
            canonical_url="https://www.inkagrowth.com/digital-marketing-in-chandausi/",
            robots_index=True,
            robots_follow=True,
        )
        self.post.internal_links.set(InternalLink.objects.all()[:4])
        self.post.outbound_links.set(OutboundLink.objects.all()[:4])

    def test_dashboard_requires_staff_login(self):
        response = self.client.get("/dashboard/posts/")
        self.assertEqual(response.status_code, 302)

        self.client.login(username="editor", password="pass")
        response = self.client.get("/dashboard/posts/")
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Posts")

    def test_published_post_uses_root_level_slug(self):
        response = self.client.get("/digital-marketing-in-chandausi/")
        self.assertEqual(response.status_code, 200)
        html = response.content.decode()
        self.assertIn("<h1>Digital Marketing in Chandausi</h1>", html)
        self.assertIn("BlogPosting", html)
        self.assertIn("BreadcrumbList", html)
        self.assertIn('<link rel="canonical"', html)

    def test_draft_post_is_not_public(self):
        self.post.status = Post.STATUS_DRAFT
        self.post.save(update_fields=["status"])

        response = self.client.get("/digital-marketing-in-chandausi/")
        self.assertEqual(response.status_code, 404)

    def test_sitemap_and_robots_include_post_rules(self):
        sitemap = self.client.get("/sitemap.xml")
        robots = self.client.get("/robots.txt")

        self.assertEqual(sitemap.status_code, 200)
        self.assertIn("sitemap-posts.xml", sitemap.content.decode())
        self.assertEqual(robots.status_code, 200)
        self.assertIn("Disallow: /dashboard/", robots.content.decode())
