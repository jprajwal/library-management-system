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
from django.urls import include, path

from library import views

urlpatterns = [
    path("", views.index, name="index"),
    path("admin/", admin.site.urls),
    path("library/books", views.BooksView.as_view(), name="library-books"),
    path(
        "library/bookcopies", views.BookCopiesView.as_view(), name="library-bookcopies"
    ),
    path(
        "library/bookcopies/<int:bookcopy_id>",
        views.BookCopyView.as_view(),
        name="library-bookcopy",
    ),
    path("accounts/signup", views.signup, name="signup"),
    path("accounts/", include("django.contrib.auth.urls")),
]
