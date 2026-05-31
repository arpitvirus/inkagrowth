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