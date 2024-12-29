import json

from django.contrib.auth.models import User
from django.http import (
    HttpRequest,
    HttpResponse,
    HttpResponseBadRequest,
    HttpResponseNotFound,
    HttpResponseServerError,
)
from django.shortcuts import redirect, render
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.csrf import csrf_exempt

from .controllers import BookCopiesController, BooksController, BooksSearchCriteria


def index(request):
    books = BooksController.browse()
    context = {"books": []}
    for i, book in enumerate(books, 1):
        book_copies_count = len(BookCopiesController.get(book_id=book.id))
        authors = ", ".join(book.author.values_list("name", flat=True))
        context["books"].append(
            {
                "id": book.id,
                "slno": i,
                "title": book.title,
                "authors": authors,
                "count": book_copies_count,
            }
        )
    return render(request, template_name="index.html", context=context)


def signup(request: HttpRequest):
    if request.method == "GET":
        return render(request, template_name="signup.html")
    username = request.POST["username"]
    password = request.POST["password"]
    email = request.POST["email"]
    try:
        _ = User.objects.create_user(username, email, password)
        return redirect("login")
    except Exception as exc:
        return HttpResponseServerError(
            json.dumps({"status": "FAILED", "error_msg": str(exc)})
        )


class BooksSearchView(View):
    def post(self, request) -> HttpResponse:
        body = request.POST
        if "searchby" in body:
            criteria = (
                BooksSearchCriteria.AUTHOR
                if body["searchby"] == "author"
                else BooksSearchCriteria.TITLE
            )
            data = BooksController.search(criteria, body["search-text"])
        else:
            data = BooksController.browse()
        context = {"books": []}
        for i, book in enumerate(data, 1):
            book_copies_count = len(BookCopiesController.get(book_id=book.id))
            authors = ", ".join(book.author.values_list("name", flat=True))
            context["books"].append(
                {
                    "id": book.id,
                    "slno": i,
                    "title": book.title,
                    "authors": authors,
                    "count": book_copies_count,
                }
            )
        return render(request, template_name="index.html", context=context)


@method_decorator(csrf_exempt, name="dispatch")
class BookCopiesView(View):
    def get(self, request) -> HttpResponse:
        queries = request.GET
        if "book_id" not in queries:
            return HttpResponseBadRequest(
                json.dumps(
                    {
                        "status": "FAILED",
                        "error": "book_id is mandatory query parameter",
                    }
                ),
                content_type="application/json",
            )
        book_id = queries["book_id"]
        data = BookCopiesController.get(int(book_id))
        return HttpResponse(
            json.dumps(
                [
                    {
                        "id": book.id,
                        "book_id": book.get_book_id(),
                    }
                    for book in data
                ]
            )
        )

    def post(self, request) -> HttpResponse:
        data = json.loads(request.body)
        try:
            BookCopiesController.create_new_copies(
                book_id=data["book_id"], count=data["count"]
            )
            return HttpResponse(
                json.dumps({"status": "OK"}), content_type="application/json"
            )
        except Exception as exc:
            return HttpResponseServerError(
                json.dumps(
                    {
                        "status": "FAILED",
                        "error": str(exc),
                    }
                ),
                content_type="application/json",
            )

    def patch(self, request) -> HttpResponse:
        data = json.loads(request.body)
        BookCopiesController.add_copies(book_id=data["book_id"], count=data["count"])
        return HttpResponse(
            json.dumps({"status": "OK"}), content_type="application/json"
        )


@method_decorator(csrf_exempt, name="dispatch")
class BookCopyView(View):
    def delete(self, request, bookcopy_id: int) -> HttpResponse:
        try:
            BookCopiesController.delete_bookcopy(bookcopy_id)
        except Exception as exc:
            return HttpResponseNotFound(
                json.dumps(
                    {
                        "status": "FAILED",
                        "error": str(exc),
                    }
                ),
                content_type="application/json",
            )
        return HttpResponse(
            json.dumps({"status": "OK"}),
            content_type="application/json",
        )
