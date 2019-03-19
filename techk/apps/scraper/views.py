import collections

from django.utils.text import slugify

from rest_framework import generics, status, mixins, viewsets, views
from rest_framework.response import Response

from apps.categories.models import Category
from apps.books.models import Book

from .utils import (
    get_categories,
    get_pages,
    get_page_books,
    get_book_info
)


class GenerateScrapeView(views.APIView):
    permission_classes = []
    authentication_classes = []

    def post(self, request):

        # get all categories from scrape
        create_categories = get_categories()

        # validate categories
        if len(create_categories) == 0:
            return Response(
                {"message": "No categories found from scrape"},
                status=status.HTTP_400_BAD_REQUEST
                )

        # create default dict
        categories_collection = collections.defaultdict(str)
        categories_count = 0

        for cat in create_categories:
            # get or create each category
            category, created_cat = Category.objects.get_or_create(name=cat)
            categories_collection.update({category.slug: category})
            # count new created categories
            if(created_cat):
                categories_count += 1

        # get all book pages
        pages = get_pages()
        if len(pages) == 0:
            return Response(
                {"message": "No pages found from scrape"},
                status=status.HTTP_400_BAD_REQUEST
                )
        
        # get all books links to get data url, thumbnail pair dict

        all_links = []
        for page in pages:
            # get url and thumbnail 
            one_page_book = get_page_books(page)
            if len(one_page_book) > 0:
                all_links = one_page_book + all_links

        if len(all_links) == 0:
            return Response(
                {"message": "No links found from scrape"},
                status=status.HTTP_400_BAD_REQUEST
                )


        books_count = 0
        for data in all_links:
            print(data)
            # get single book info
            one_book = get_book_info(data)
            if bool(one_book):
                print("creating books")
                # get category
                book_category = categories_collection.get(slugify(one_book['category']))
                # create new book
                new_book, created_book = Book.objects.get_or_create(
                    upc=one_book['upc'],
                    defaults = {
                        'category': book_category,
                        'title': one_book['title'],
                        'thumbnail_url': one_book['thumbnail_url'],
                        'price': one_book['price'],
                        'stock': one_book['stock'],
                        'product_description': one_book['product_description'],
                    }
                )

                if created_book:
                    books_count +=1
        
        return Response({
            'message': f"categories created: {categories_count}, Books created: {books_count}"
            })

