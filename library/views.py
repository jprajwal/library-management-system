# from django.shortcuts import render
from django.core import serializers
from .controllers import BookCatalog
from django.http import HttpResponse


# Create your views here.
def library_book_catalog_browse(request):
    data = serializers.serialize('json', BookCatalog.browse())
    return HttpResponse(data, content_type="application/json")
