from django.db import models


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
