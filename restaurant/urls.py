from django.urls import include, path
from rest_framework.authtoken.views import obtain_auth_token
from rest_framework.routers import SimpleRouter

from . import views

router = SimpleRouter()
router.register("api/menu", views.MenuItemsViewSet, basename="menu")
router.register("api/bookings", views.BookingViewSet, basename="booking")

urlpatterns = [
    # Static HTML pages
    path("", views.home, name="home"),
    path("about/", views.about, name="about"),
    path("menu/", views.menu_page, name="menu-page"),
    path("book/", views.book_page, name="book"),
    # API
    path("api-token-auth/", obtain_auth_token, name="api-token-auth"),
    path("api/me/", views.MeView.as_view(), name="api-me"),
    path("", include(router.urls)),
]
