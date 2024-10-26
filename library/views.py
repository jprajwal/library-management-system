# from django.shortcuts import render
from django.views import View
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator

import json

from .controllers import BookCatalog, BookCatalogSearchCriteria


# Create your views here.
@method_decorator(csrf_exempt, name='dispatch')
class CatalogBooksView(View):
    def get(self, request) -> HttpResponse:
        queries = request.GET
        if "author" in queries:
            data = BookCatalog.search(BookCatalogSearchCriteria.AUTHOR, queries["author"])
        elif "title" in queries:
            data = BookCatalog.search(BookCatalogSearchCriteria.TITLE, queries["title"])
        else:
            data = BookCatalog.browse()
        return HttpResponse(json.dumps([
                {
                    "title": book.title,
                    "author": book.get_author_ids(),
                    "rent_cost": book.rent_cost,
                    "max_rent_period": book.get_max_rent_period_as_int(),
                } for book in data
        ]))

    def post(self, request) -> HttpResponse:
        data = json.loads(request.body)
        BookCatalog.add_book(**data)
        return HttpResponse(json.dumps({"status": "OK"}), content_type="application/json")
