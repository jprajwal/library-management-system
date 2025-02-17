import json
from typing import Any

from django.contrib.auth.models import User
from django.db.models import F
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
    AllBookDataGetter,
    BookCopiesController,
    CartItemsController,
    FilteredBookDataGetter,
    OrderedBookDataGetter,
    FilteredCartItemDataGetter,
    AllCartItemDataGetter,
)
from .models import Book, CartItem
from .pagination import PaginatedData, Pagination


class Utils:
    @staticmethod
    def get_pagination_view(request: HttpRequest, pd: PaginatedData) -> tuple[str, str]:
        page = int(request.GET.get("page", GC.default_page))
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
        return (prev_link, next_link)

    @staticmethod
    def get_filter_protocol_info(
        request, filter_keys: list[str]
    ) -> dict[str, Any] | None:
        if any(map(lambda x: x in filter_keys, request.GET.keys())):
            filters = {}
            matchby = request.GET.get("matchby", "contains")
            for key in filter_keys:
                if key in request.GET:
                    filters.update(
                        {
                            key: {
                                "matchby": matchby,
                                "value": request.GET[key],
                            }
                        }
                    )
            return filters
        return None


def index(request):
    return render(request, template_name="index.html")


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
        data = AllBookDataGetter().get_data(None)
        page = int(request.GET.get("page") or GC.default_page)
        perpage = int(request.GET.get("per_page") or GC.default_perpage)

        # order
        data = data.transform_if(
            lambda: "order" in request.GET,
            OrderedBookDataGetter(request.GET.get("order", "ascend")),
        )

        # filter
        filters = Utils.get_filter_protocol_info(request, ["author", "title"])
        print(f"{filters=}")
        data = data.transform_if(
            lambda: filters is not None, FilteredBookDataGetter(filters or {})
        )

        pagination = Pagination[Book](data)
        pd = pagination.paginate(page, perpage)
        prev_link, next_link = Utils.get_pagination_view(request, pd)

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


# /library/members/me/cartitems
class CartItemsView(View):
    def get(self, request: HttpRequest) -> HttpResponse:
        if not request.user.is_authenticated:
            return HttpResponse(
                json.dumps(
                    {
                        "status": "FAILED",
                        "error_name": "UnauthorizedError",
                        "error_msg": "you must be authenticated to access this resource",
                    }
                )
            )
        page = int(request.GET.get("page") or GC.default_page)
        perpage = int(request.GET.get("per_page") or GC.default_perpage)

        data = AllCartItemDataGetter().get_data(None)
        data = data.transform(
            FilteredCartItemDataGetter(
                {"userid": {"matchby": "exact", "value": request.user.id}}
            )
        )
        pd = Pagination(data).paginate(page, perpage)
        prev_link, next_link = Utils.get_pagination_view(request, pd)
        return HttpResponse(
            json.dumps(
                {
                    "cart_items": list(pd.items),
                    "prev": prev_link,
                    "next": next_link,
                },
                cls=serde.CartItemEncoder,
            )
        )

    # /library/members/me/cartitems
    def post(self, request: HttpRequest) -> HttpResponse:
        if not request.user.is_authenticated:
            return HttpResponse(
                json.dumps(
                    {
                        "status": "FAILED",
                        "error_name": "UnauthorizedError",
                        "error_msg": "you must be authenticated to access this resource",
                    }
                )
            )
        data = json.loads(request.body.decode("utf-8"))
        item_info = data["item_info"]
        matches = CartItem.objects.filter(userid=request.user.id).filter(product_id=item_info["id"])
        if matches.count() == 0:
            # create item
            pass
        else:
            matches[0].requested_count += 1
            matches[0].save()



# /library/members/me/cartitems
# class CartItemsView(View):
#     def get(self, request: HttpRequest) -> HttpResponse:
#         if not request.user.is_authenticated:
#             return HttpResponse(json.dumps({
#                 "status": "FAILED",
#                 "error_name": "UnauthorizedError",
#                 "error_msg": "you must be authenticated to access this resource"
#             }))
#         cart_items = CartItemsController.get_cartitems(request.user)
#         print(cart_items)
#         context = {"cart_items": []}
#         for i, item in enumerate(cart_items, 1):
#             book = item.book_copy.book_id
#             authors = ", ".join(book.author.values_list("name", flat=True))
#             context["cart_items"].append(
#                 {
#                     "cartitem_id": item.id,
#                     "book_id": book.id,
#                     "slno": i,
#                     "title": book.title,
#                     "authors": authors,
#                     "added_on": item.added_on,
#                 }
#             )

#         return render(request, template_name="cart.html", context=context)

#     def post(self, request: HttpRequest, userid: int) -> HttpResponse:
#         print(f"{userid=}, {request.user.id=}")
#         if userid != request.user.id:
#             return HttpResponseForbidden(
#                 "as of now, only self userid is permitted by the server."
#             )
#         body = json.loads(request.body.decode("utf-8"))
#         if "bookid" not in body:
#             return HttpResponseBadRequest("bookid not provided in the request")
#         bookid = body["bookid"]
#         book_copies = BookCopiesController.get(book_id=bookid)
#         if len(book_copies) == 0:
#             return HttpResponse("Book copies not available", status=409)
#         CartItemsController.add_cartitem(request.user, book_copies[0].id)
#         return HttpResponse("Successful")


class CartItemView(View):
    def delete(self, request: HttpRequest, userid: int, itemid: int) -> HttpResponse:
        if userid != request.user.id:
            return HttpResponseForbidden(
                "as of now, only self userid is permitted by the server."
            )
        CartItemsController.delete_cartitem(request.user, itemid)
        return HttpResponse("Successful")
