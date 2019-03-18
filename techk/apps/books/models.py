from django.db import models


class Book(models.Model):
    """
    Book model

    Book representation, it belongs to one Category
    """

    # Unique key
    upc = models.CharField(max_length=100, unique=True, blank=False, null=False)
    # Foreign key
    category = models.ForeignKey(
        "categories.Category", on_delete=models.CASCADE, related_name="books"
    )
    title = models.CharField(max_length=255, blank=False, null=False)
    thumbnail_url = models.URLField(max_length=255)
    price = models.FloatField()
    stock = models.IntegerField()
    product_description = models.TextField(blank=True, null=True)

    class Meta:
        ordering = ["-id"]
        get_latest_by = "upc"

    def __str__(self):
        return "{}".format(self.upc)
