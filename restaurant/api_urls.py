from django.urls import include, path
from rest_framework.authtoken.views import obtain_auth_token
from rest_framework.routers import DefaultRouter

from . import views

router = DefaultRouter()
router.register(r"bookings", views.BookingViewSet, basename="booking")

urlpatterns = [
    path("menu/", views.MenuItemsView.as_view(), name="api-menu"),
    path("menu/<int:pk>/", views.SingleMenuItemView.as_view(), name="api-menu-item"),
    path("registration/", views.RegistrationView.as_view(), name="api-registration"),
    path("token/", obtain_auth_token, name="api-token"),
    path("me/", views.MeView.as_view(), name="api-me"),
    path("", include(router.urls)),
]
