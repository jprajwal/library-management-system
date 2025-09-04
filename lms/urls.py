"""
URL configuration for lms project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.contrib.auth.views import LoginView, LogoutView
from django.urls import path

from library import views

urlpatterns = [
    path("", views.index, name="index"),

    # admin/
    path("admin/", admin.site.urls),

    # accounts/
    path("accounts/signup", views.signup, name="signup"),
    path(
        "accounts/login",
        view=LoginView.as_view(template_name="login.html"),
        name="login",
    ),
    path("accounts/logout", view=LogoutView.as_view(), name="logout"),

    # library/
    path(
        "library/members/me/cartitems",
        view=views.CartItemsView.as_view(), name="cart-items",
    ),
    path(
        "library/members/<int:userid>/cartitems/<int:itemid>",
        view=views.CartItemView.as_view(), name="cart-item",
    ),
    path("library/books", views.BooksView.as_view(), name="books-view"),
    path("library/lend-books", views.lend_books, name="lend-books"),
    path("library/return-books", views.return_books, name="return-books"),
    path("library/update-payment", views.update_payment, name="update-payment"),
    path("library/borrowed-books", views.get_borrowed_books_of_user, name="borrowed-books"),
]
