from django.urls import path

from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("about/", views.about, name="about"),
    path("menu/", views.menu_page, name="menu"),
    path("book/", views.book_page, name="book"),
]
