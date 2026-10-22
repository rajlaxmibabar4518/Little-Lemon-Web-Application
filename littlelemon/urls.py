from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path("admin/", admin.site.urls),
    # Djoser endpoints: user registration (/auth/users/) and token login (/auth/token/login/)
    path("auth/", include("djoser.urls")),
    path("auth/", include("djoser.urls.authtoken")),
    path("", include("restaurant.urls")),
]
