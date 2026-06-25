from django.db import models
from django.urls import reverse
from django.utils.text import slugify


class contact(models.Model):
    name = models.CharField(max_length=30)
    email = models.CharField(max_length=35)
    mobile = models.CharField(max_length=13)
    message = models.TextField(blank=True, help_text="Enter your comments here.")

    class Meta:
        verbose_name = "Contact"
        verbose_name_plural = "Contacts"

    def __str__(self):
        return self.name


class PortfolioProject(models.Model):
    STATUS_ONGOING = "ongoing"
    STATUS_COMPLETED = "completed"

    STATUS_CHOICES = (
        (STATUS_ONGOING, "Ongoing"),
        (STATUS_COMPLETED, "Completed"),
    )

    SERVICE_GOOGLE_MAPS_SEO = "google-maps-seo"
    SERVICE_SOCIAL_MEDIA = "social-media-management"
    SERVICE_META_ADS = "meta-ads"
    SERVICE_WEBSITE = "website-development"
    SERVICE_BRANDING = "branding"
    SERVICE_LEAD_GENERATION = "lead-generation"
    SERVICE_LOCAL_SEO = "local-seo"
    SERVICE_COMPLETE_MARKETING = "complete-digital-marketing"

    SERVICE_TYPE_CHOICES = (
        (SERVICE_GOOGLE_MAPS_SEO, "Google Maps SEO"),
        (SERVICE_SOCIAL_MEDIA, "Social Media Management"),
        (SERVICE_META_ADS, "Meta Ads"),
        (SERVICE_WEBSITE, "Website Development"),
        (SERVICE_BRANDING, "Branding"),
        (SERVICE_LEAD_GENERATION, "Lead Generation"),
        (SERVICE_LOCAL_SEO, "Local SEO"),
        (SERVICE_COMPLETE_MARKETING, "Complete Digital Marketing"),
    )

    business_name = models.CharField(max_length=180)
    slug = models.SlugField(max_length=220, unique=True, blank=True)
    business_category = models.CharField(max_length=180)
    location = models.CharField(max_length=180)
    short_description = models.TextField()
    cover_image = models.ImageField(upload_to="portfolio/covers/", blank=True)
    client_logo = models.ImageField(upload_to="portfolio/logos/", blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default=STATUS_ONGOING, db_index=True)
    is_featured = models.BooleanField(default=False, db_index=True)
    display_order = models.PositiveIntegerField(default=0, db_index=True)

    services_provided = models.TextField(blank=True)
    service_type = models.CharField(max_length=40, choices=SERVICE_TYPE_CHOICES, db_index=True)

    client_overview = models.TextField(blank=True)
    problem = models.TextField(blank=True)
    strategy = models.TextField(blank=True)
    work_done = models.TextField(blank=True)
    keywords_targeted = models.TextField(blank=True)
    result_summary = models.TextField(blank=True)
    before_inkagrowth = models.TextField(blank=True)
    after_inkagrowth = models.TextField(blank=True)

    keywords_targeted_count = models.PositiveIntegerField(blank=True, null=True)
    search_visibility = models.CharField(max_length=120, blank=True)
    profile_views = models.PositiveIntegerField(blank=True, null=True)
    direction_requests = models.PositiveIntegerField(blank=True, null=True)
    calls_received = models.PositiveIntegerField(blank=True, null=True)
    leads_generated = models.PositiveIntegerField(blank=True, null=True)
    campaigns_run = models.PositiveIntegerField(blank=True, null=True)

    website_url = models.URLField(blank=True)
    instagram_url = models.URLField(blank=True)
    facebook_url = models.URLField(blank=True)
    google_maps_url = models.URLField(blank=True)

    testimonial_text = models.TextField(blank=True)
    testimonial_person_name = models.CharField(max_length=140, blank=True)
    testimonial_person_designation = models.CharField(max_length=160, blank=True)

    meta_title = models.CharField(max_length=255, blank=True)
    meta_description = models.TextField(blank=True)
    focus_keyword = models.CharField(max_length=180, blank=True)
    canonical_url = models.URLField(blank=True)
    og_title = models.CharField(max_length=255, blank=True)
    og_description = models.TextField(blank=True)
    og_image = models.ImageField(upload_to="portfolio/og/", blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ("display_order", "-updated_at", "business_name")
        indexes = [
            models.Index(fields=("status", "display_order"), name="front_portfolio_status_idx"),
            models.Index(fields=("service_type", "status"), name="front_portfolio_service_idx"),
            models.Index(fields=("slug", "status"), name="front_portfolio_slug_idx"),
        ]
        verbose_name = "Portfolio Project"
        verbose_name_plural = "Portfolio Projects"

    def __str__(self):
        return self.business_name

    @classmethod
    def live(cls):
        return cls.objects.filter(status__in=[cls.STATUS_ONGOING, cls.STATUS_COMPLETED])

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = self._generate_unique_slug()
        super().save(*args, **kwargs)

    def _generate_unique_slug(self):
        base_slug = slugify(self.business_name) or "portfolio-project"
        slug = base_slug
        counter = 2
        queryset = PortfolioProject.objects.all()
        if self.pk:
            queryset = queryset.exclude(pk=self.pk)

        while queryset.filter(slug=slug).exists():
            slug = f"{base_slug}-{counter}"
            counter += 1
        return slug

    def get_absolute_url(self):
        return reverse("portfolio_detail", kwargs={"slug": self.slug})

    @property
    def seo_title(self):
        return self.meta_title or (
            f"{self.business_name} Case Study | {self.business_category} in {self.location} | Inkagrowth"
        )

    @property
    def seo_description(self):
        if self.meta_description:
            return self.meta_description
        services = self.services_provided or self.get_service_type_display()
        return (
            f"See how Inkagrowth supports {self.business_name}, a {self.business_category} "
            f"in {self.location}, with {services}."
        )
