from django.test import TestCase, override_settings

from .models import contact


@override_settings(ALLOWED_HOSTS=["testserver"], SECURE_SSL_REDIRECT=False)
class FrontPageTests(TestCase):
    def test_homepage_renders(self):
        response = self.client.get("/")

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "INKAGROWTH Digital Marketing Agency")

    def test_contact_page_renders(self):
        response = self.client.get("/contact/")

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Contact InkaGROWTH")

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
        self.assertEqual(robots.status_code, 200)
