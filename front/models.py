from django.conf import settings
from django.db import models
from django.urls import reverse
from django.utils import timezone

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


class Category(models.Model):
    name = models.CharField(max_length=120, unique=True)
    slug = models.SlugField(unique=True)
    description = models.TextField(blank=True)
    is_indexable = models.BooleanField(default=True)

    class Meta:
        ordering = ("name",)
        verbose_name_plural = "categories"

    def __str__(self):
        return self.name


class Tag(models.Model):
    name = models.CharField(max_length=120, unique=True)
    slug = models.SlugField(unique=True)
    is_indexable = models.BooleanField(default=True)

    class Meta:
        ordering = ("name",)

    def __str__(self):
        return self.name


class AuthorProfile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    display_name = models.CharField(max_length=120)
    bio = models.TextField(blank=True)
    avatar = models.ImageField(upload_to="authors/", blank=True)

    def __str__(self):
        return self.display_name


class MediaFile(models.Model):
    title = models.CharField(max_length=160)
    file = models.ImageField(upload_to="post-media/")
    alt_text = models.CharField(max_length=180, blank=True)
    uploaded_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ("-created_at",)

    def __str__(self):
        return self.title


class Post(models.Model):
    STATUS_DRAFT = "draft"
    STATUS_PUBLISHED = "published"
    STATUS_SCHEDULED = "scheduled"
    STATUS_CHOICES = (
        (STATUS_DRAFT, "Draft"),
        (STATUS_PUBLISHED, "Published"),
        (STATUS_SCHEDULED, "Scheduled"),
    )

    title = models.CharField(max_length=180)
    slug = models.SlugField(unique=True)
    focus_keyphrase = models.CharField(max_length=160, blank=True)
    meta_title = models.CharField(max_length=60, blank=True)
    meta_description = models.CharField(max_length=160, blank=True)
    excerpt = models.TextField(blank=True)
    content = models.TextField(blank=True)
    featured_image = models.ForeignKey(MediaFile, on_delete=models.SET_NULL, null=True, blank=True, related_name="featured_posts")
    featured_image_alt = models.CharField(max_length=180, blank=True)
    category = models.ForeignKey(Category, on_delete=models.PROTECT, null=True, blank=True, related_name="posts")
    tags = models.ManyToManyField(Tag, blank=True, related_name="posts")
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, related_name="front_posts")
    service = models.CharField(max_length=120, blank=True)
    city = models.CharField(max_length=120, blank=True)
    state = models.CharField(max_length=120, blank=True)
    status = models.CharField(max_length=16, choices=STATUS_CHOICES, default=STATUS_DRAFT, db_index=True)
    published_at = models.DateTimeField(null=True, blank=True)
    scheduled_at = models.DateTimeField(null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True)
    canonical_url = models.URLField(max_length=255, blank=True)
    robots_index = models.BooleanField(default=True)
    robots_follow = models.BooleanField(default=True)
    og_title = models.CharField(max_length=180, blank=True)
    og_description = models.CharField(max_length=220, blank=True)
    og_image = models.ForeignKey(MediaFile, on_delete=models.SET_NULL, null=True, blank=True, related_name="og_posts")
    twitter_title = models.CharField(max_length=180, blank=True)
    twitter_description = models.CharField(max_length=220, blank=True)
    twitter_image = models.ForeignKey(MediaFile, on_delete=models.SET_NULL, null=True, blank=True, related_name="twitter_posts")
    schema_type = models.CharField(max_length=40, default="BlogPosting")
    reading_time = models.PositiveIntegerField(default=1)
    word_count = models.PositiveIntegerField(default=0)
    seo_score = models.PositiveIntegerField(default=0)
    readability_score = models.PositiveIntegerField(default=0)
    internal_links = models.ManyToManyField(InternalLink, blank=True, related_name="posts")
    outbound_links = models.ManyToManyField(OutboundLink, blank=True, related_name="posts")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ("-published_at", "-updated_at")
        indexes = [
            models.Index(fields=("status", "published_at")),
            models.Index(fields=("slug", "status")),
        ]

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("post_detail", kwargs={"slug": self.slug})

    @property
    def is_public(self):
        return self.status == self.STATUS_PUBLISHED and self.robots_index and (
            self.published_at is None or self.published_at <= timezone.now()
        )


class FAQ(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="faqs")
    question = models.CharField(max_length=220)
    answer = models.TextField()
    sort_order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ("sort_order", "id")

    def __str__(self):
        return self.question


class SEOAnalysisResult(models.Model):
    post = models.OneToOneField(Post, on_delete=models.CASCADE, related_name="analysis")
    seo_checks = models.JSONField(default=list, blank=True)
    readability_checks = models.JSONField(default=list, blank=True)
    seo_score = models.PositiveIntegerField(default=0)
    readability_score = models.PositiveIntegerField(default=0)
    analyzed_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"SEO analysis for {self.post}"
