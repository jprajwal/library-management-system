import json

from django.contrib.auth.models import User
from django.http import (
    HttpRequest,
    HttpResponse,
    HttpResponseBadRequest,
    HttpResponseForbidden,
    HttpResponseServerError,
)
from django.shortcuts import redirect, render
from django.utils import http as httputils
from django.views import View

from . import serde
from .constants import GlobalConstants as GC
from .controllers import (
    BookCopiesController,
    BooksController,
    CartItemsController,
    FilteredBookDataGetter,
    OrderedBookDataGetter,
)
from .models import Book
from .pagination import Pagination


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


# /library/books?page=1&per_page=50
class BooksView(View):
    def get(self, request: HttpRequest) -> HttpResponse:
        data = BooksController.get_all()
        page = int(request.GET.get("page") or GC.default_page)
        perpage = int(request.GET.get("per_page") or GC.default_perpage)

        # order
        if "order" in request.GET:
            data = data.apply(OrderedBookDataGetter(request.GET["order"]).get_data)

        # filter
        if any(map(lambda x: x in ["author", "title"], request.GET.keys())):
            filters = {}
            matchby = request.GET.get("matchby", "contains")
            if "author" in request.GET:
                filters.update(
                    {
                        "author__name": {
                            "matchby": matchby,
                            "value": request.GET["author"],
                        }
                    }
                )
            if "title" in request.GET:
                filters.update(
                    {"title": {"matchby": matchby, "value": request.GET["title"]}}
                )
            print(f"{filters=}")
            data = data.apply(FilteredBookDataGetter(filters).get_data)

        pagination = Pagination[Book](data)

        pd = pagination.paginate(page, perpage)

        prev_link = ""
        next_link = ""
        if pd.has_next:
            q = dict(**request.GET)
            q["page"] = page + 1
            next_link = f"{request.path}?{httputils.urlencode(q, doseq=True)}"

        if pd.has_prev:
            q = dict(**request.GET)
            q["page"] = page - 1
            prev_link = f"{request.path}?{httputils.urlencode(q, doseq=True)}"

        return HttpResponse(
            json.dumps(
                {
                    "books": list(pd.items),
                    "next": next_link,
                    "prev": prev_link,
                },
                cls=serde.BookEncoder,
            )
        )


# /library/members/<str:username>/cartitems
class CartItemsView(View):
    def get(self, request: HttpRequest, userid: int) -> HttpResponse:
        if userid != request.user.id:
            return HttpResponseForbidden(
                "as of now, only username=self is permitted by the server."
            )
        if not request.user.is_authenticated:
            # TODO: handle this case in a more sophisticated way.
            return HttpResponse("Unauthorized", status=401)
        cart_items = CartItemsController.get_cartitems(request.user)
        print(cart_items)
        context = {"cart_items": []}
        for i, item in enumerate(cart_items, 1):
            book = item.book_copy.book_id
            authors = ", ".join(book.author.values_list("name", flat=True))
            context["cart_items"].append(
                {
                    "cartitem_id": item.id,
                    "book_id": book.id,
                    "slno": i,
                    "title": book.title,
                    "authors": authors,
                    "added_on": item.added_on,
                }
            )

        return render(request, template_name="cart.html", context=context)

    def post(self, request: HttpRequest, userid: int) -> HttpResponse:
        print(f"{userid=}, {request.user.id=}")
        if userid != request.user.id:
            return HttpResponseForbidden(
                "as of now, only self userid is permitted by the server."
            )
        body = json.loads(request.body.decode("utf-8"))
        if "bookid" not in body:
            return HttpResponseBadRequest("bookid not provided in the request")
        bookid = body["bookid"]
        book_copies = BookCopiesController.get(book_id=bookid)
        if len(book_copies) == 0:
            return HttpResponse("Book copies not available", status=409)
        CartItemsController.add_cartitem(request.user, book_copies[0].id)
        return HttpResponse("Successful")


class CartItemView(View):
    def delete(self, request: HttpRequest, userid: int, itemid: int) -> HttpResponse:
        if userid != request.user.id:
            return HttpResponseForbidden(
                "as of now, only self userid is permitted by the server."
            )
        CartItemsController.delete_cartitem(request.user, itemid)
        return HttpResponse("Successful")
