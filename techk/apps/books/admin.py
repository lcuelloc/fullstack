from django.contrib import admin

from apps.books.models import Book


@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    pass
