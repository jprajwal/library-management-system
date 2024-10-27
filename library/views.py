# from django.shortcuts import render
from django.views import View
from django.http import HttpResponse, HttpResponseBadRequest, HttpResponseServerError
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator

import json

from .controllers import BooksController, BooksSearchCriteria, BookCopiesController


# Create your views here.
@method_decorator(csrf_exempt, name='dispatch')
class BooksView(View):
    def get(self, request) -> HttpResponse:
        queries = request.GET
        if "author" in queries:
            data = BooksController.search(BooksSearchCriteria.AUTHOR, queries["author"])
        elif "title" in queries:
            data = BooksController.search(BooksSearchCriteria.TITLE, queries["title"])
        else:
            data = BooksController.browse()
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
        BooksController.add_book(**data)
        return HttpResponse(json.dumps({"status": "OK"}), content_type="application/json")


@method_decorator(csrf_exempt, name='dispatch')
class BookCopiesView(View):
    def get(self, request) -> HttpResponse:
        queries = request.GET
        if "book_id" not in queries:
            return HttpResponseBadRequest(
                json.dumps({
                    "status": "FAILED", "error": "book_id is mandatory query parameter"
                }),
                content_type="application/json",
            )
        book_id = queries["book_id"]
        data = BookCopiesController.get(int(book_id))
        return HttpResponse(json.dumps([
                {
                    "id": book.id,
                    "book_id": book.get_book_id(),
                } for book in data
        ]))

    def post(self, request) -> HttpResponse:
        data = json.loads(request.body)
        try:
            BookCopiesController.create_new_copies(book_id=data["book_id"], count=data["count"])
            return HttpResponse(json.dumps({"status": "OK"}), content_type="application/json")
        except Exception as exc:
            return HttpResponseServerError(
                json.dumps({
                    "status": "FAILED", "error": str(exc),
                }),
                content_type="application/json",
            )
            

    def patch(self, request) -> HttpResponse:
        data = json.loads(request.body)
        BookCopiesController.add_copies(book_id=data["book_id"], count=data["count"])
        return HttpResponse(json.dumps({"status": "OK"}), content_type="application/json")