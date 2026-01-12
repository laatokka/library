from django.db import models

class Location(models.Model):
    slug = models.SlugField(unique=True, help_text="Crucial: This must match the id of the elements in our SVG map.")
    display_name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.display_name
