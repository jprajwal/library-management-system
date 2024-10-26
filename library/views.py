# from django.shortcuts import render
from django.core import serializers
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
        data = serializers.serialize('json', data)
        return HttpResponse(data, content_type="application/json")

    def post(self, request) -> HttpResponse:
        data = json.loads(request.body)
        BookCatalog.add_book(**data)
        return HttpResponse(json.dumps({"status": "OK"}), content_type="application/json")
