from django.db import models
from django.dispatch import receiver
from django.utils.text import slugify


class Category(models.Model):
    """
    Category model

    A Category classification can have many associated Books
    """
    name = models.CharField(max_length=255, blank=False, null=False)
    slug = models.CharField(max_length=255, unique=True)

    class Meta:
        ordering = ["-id"]
        get_latest_by = "name"

    def __str__(self):
        return "{}".format(self.name)


@receiver(models.signals.post_save, sender=Category)
def create_internal_code(sender, instance, created, *args, **kwargs):
    """ Slug generator"""
    if created and instance.name:
        instance.slug = slugify(instance.name)
        instance.save()
