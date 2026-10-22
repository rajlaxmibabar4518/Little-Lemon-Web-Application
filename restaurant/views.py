from django.contrib.auth.models import User
from django.shortcuts import render
from rest_framework import generics, permissions, viewsets
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Booking, Menu
from .serializers import BookingSerializer, MenuSerializer, RegistrationSerializer


# ---------------------------------------------------------------------------
# Static HTML pages served by Django
# ---------------------------------------------------------------------------
def home(request):
    return render(request, "restaurant/index.html")


def about(request):
    return render(request, "restaurant/about.html")


def menu_page(request):
    return render(request, "restaurant/menu.html", {"menu": Menu.objects.all()})


def book_page(request):
    return render(request, "restaurant/book.html")


# ---------------------------------------------------------------------------
# REST API
# ---------------------------------------------------------------------------
class MenuItemsView(generics.ListCreateAPIView):
    queryset = Menu.objects.all()
    serializer_class = MenuSerializer
    search_fields = ["title"]


class SingleMenuItemView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Menu.objects.all()
    serializer_class = MenuSerializer


class BookingViewSet(viewsets.ModelViewSet):
    queryset = Booking.objects.all()
    serializer_class = BookingSerializer
    permission_classes = [permissions.IsAuthenticated]


class RegistrationView(generics.CreateAPIView):
    """Create a user account and return an auth token."""

    queryset = User.objects.all()
    serializer_class = RegistrationSerializer
    permission_classes = [permissions.AllowAny]

    def create(self, request, *args, **kwargs):
        response = super().create(request, *args, **kwargs)
        user = User.objects.get(pk=response.data["id"])
        token, _ = Token.objects.get_or_create(user=user)
        response.data["token"] = token.key
        return response


class MeView(APIView):
    """Protected endpoint used to confirm authentication works."""

    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        return Response(
            {"username": request.user.username, "email": request.user.email}
        )
