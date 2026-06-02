from django.db import models

# Create your models here.

class contact(models.Model):
    name = models.CharField(max_length=30)
    email = models.CharField(max_length=35)
    mobile = models.CharField(max_length=13)
    message = models.TextField(blank=True, help_text="Enter your comments here.")


class SEOPage(models.Model):
    city = models.CharField(max_length=100)
    service = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)
    meta_title = models.CharField(max_length=200)
    meta_description = models.TextField()
    content = models.TextField()

    def __str__(self):
        return f"{self.service} - {self.city}"


class SEOPageTemplate(models.Model):
    service = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    primary_keyword = models.CharField(max_length=160, unique=True)
    slug = models.SlugField(unique=True)
    meta_title = models.CharField(max_length=60)
    meta_description = models.CharField(max_length=160)
    content_blocks = models.JSONField(default=dict, blank=True)
    nearby_areas = models.JSONField(default=list, blank=True)
    faqs = models.JSONField(default=list, blank=True)
    is_published = models.BooleanField(default=True)

    class Meta:
        ordering = ("service", "city")
        constraints = [
            models.UniqueConstraint(
                fields=("service", "city"),
                name="unique_seo_page_template_service_city",
            )
        ]

    def __str__(self):
        return f"{self.service} in {self.city}"


class InternalLink(models.Model):
    title = models.CharField(max_length=120)
    url = models.CharField(max_length=255, unique=True)
    category = models.CharField(max_length=80, default="general", db_index=True)

    class Meta:
        ordering = ("category", "title")

    def __str__(self):
        return self.title


class OutboundLink(models.Model):
    title = models.CharField(max_length=120)
    url = models.URLField(max_length=255, unique=True)
    category = models.CharField(max_length=80, default="general", db_index=True)

    class Meta:
        ordering = ("category", "title")

    def __str__(self):
        return self.title
