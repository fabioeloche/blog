"""
Models for the about application.
"""
from django.db import models


class About(models.Model):
    """
    Model representing the About page content.

    Attributes:
        title: The title of the About page
        content: Rich text content of the About page
        updated_on: Timestamp when content was last updated
        image: Optional image for the About page
    """
    title = models.CharField(max_length=200)
    content = models.TextField()
    updated_on = models.DateTimeField(auto_now=True)
    image = models.ImageField(upload_to='about_images/', blank=True, null=True)

    class Meta:
        verbose_name = 'About'
        verbose_name_plural = 'About'

    def __str__(self):
        """String representation of the About page."""
        return self.title

    def save(self, *args, **kwargs):
        """Override save method to ensure only one About instance exists."""
        if not self.pk and About.objects.exists():
            # If this is a new instance and another one exists, don't save
            return
        super().save(*args, **kwargs)
