from django.shortcuts import render
from rest_framework import permissions, viewsets
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Booking, Menu
from .serializers import BookingSerializer, MenuSerializer


# ---------------------------------------------------------------------------
# Static HTML pages served by Django
# ---------------------------------------------------------------------------
def home(request):
    return render(request, "index.html")


def about(request):
    return render(request, "about.html")


def menu_page(request):
    return render(request, "menu.html", {"menu": Menu.objects.all()})


def book_page(request):
    return render(request, "book.html")


# ---------------------------------------------------------------------------
# REST API viewsets
# ---------------------------------------------------------------------------
class MenuItemsViewSet(viewsets.ModelViewSet):
    """Menu CRUD. Anyone can read; creating/changing needs a token."""

    queryset = Menu.objects.all()
    serializer_class = MenuSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]


class BookingViewSet(viewsets.ModelViewSet):
    """Booking CRUD. Requires authentication."""

    queryset = Booking.objects.all()
    serializer_class = BookingSerializer
    permission_classes = [permissions.IsAuthenticated]


class MeView(APIView):
    """Protected endpoint used to confirm authentication works."""

    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        return Response({"username": request.user.username, "email": request.user.email})
