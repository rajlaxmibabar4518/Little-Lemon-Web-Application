from datetime import date
from decimal import Decimal

from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse
from rest_framework.authtoken.models import Token
from rest_framework.test import APIClient

from .models import Booking, Menu
from .serializers import MenuSerializer


class ModelTests(TestCase):
    def test_menu_str(self):
        item = Menu.objects.create(title="IceCream", price=Decimal("80.00"), inventory=100)
        self.assertEqual(str(item), "IceCream : 80.00")

    def test_booking_str(self):
        booking = Booking.objects.create(
            first_name="Ana", reservation_date=date(2026, 11, 1), reservation_slot=18
        )
        self.assertEqual(str(booking), "Ana - 2026-11-01 @ 18:00")


class SerializerTests(TestCase):
    def test_menu_serializer_output(self):
        item = Menu.objects.create(title="Greek Salad", price=Decimal("12.50"), inventory=20)
        data = MenuSerializer(item).data
        self.assertEqual(data["title"], "Greek Salad")
        self.assertEqual(data["price"], "12.50")
        self.assertEqual(data["inventory"], 20)


class StaticPageTests(TestCase):
    def test_pages_render_html(self):
        for name in ("home", "about", "menu", "book"):
            response = self.client.get(reverse(name))
            self.assertEqual(response.status_code, 200)
            self.assertContains(response, "Little Lemon")

    def test_menu_page_lists_items(self):
        Menu.objects.create(title="Bruschetta", price=Decimal("7.00"), inventory=5)
        response = self.client.get(reverse("menu"))
        self.assertContains(response, "Bruschetta")


class MenuAPITests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user("chef", password="StrongPass!234")
        self.token = Token.objects.create(user=self.user)
        self.item = Menu.objects.create(title="Pasta", price=Decimal("15.00"), inventory=10)

    def test_list_is_public(self):
        response = self.client.get("/api/menu/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json()), 1)

    def test_retrieve_single_item(self):
        response = self.client.get(f"/api/menu/{self.item.pk}/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["title"], "Pasta")

    def test_create_requires_auth(self):
        payload = {"title": "Soup", "price": "6.00", "inventory": 3}
        self.assertEqual(self.client.post("/api/menu/", payload).status_code, 401)

    def test_create_update_delete_with_token(self):
        self.client.credentials(HTTP_AUTHORIZATION=f"Token {self.token.key}")
        created = self.client.post(
            "/api/menu/", {"title": "Soup", "price": "6.00", "inventory": 3}, format="json"
        )
        self.assertEqual(created.status_code, 201)
        pk = created.json()["id"]
        updated = self.client.put(
            f"/api/menu/{pk}/", {"title": "Soup", "price": "7.00", "inventory": 3}, format="json"
        )
        self.assertEqual(updated.status_code, 200)
        self.assertEqual(Menu.objects.get(pk=pk).price, Decimal("7.00"))
        self.assertEqual(self.client.delete(f"/api/menu/{pk}/").status_code, 204)


class BookingAPITests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user("guest", password="StrongPass!234")
        self.payload = {"first_name": "Sam", "reservation_date": "2026-12-01", "reservation_slot": 19}

    def test_bookings_require_auth(self):
        self.assertEqual(self.client.get("/api/bookings/").status_code, 401)

    def test_create_and_list_booking(self):
        self.client.force_authenticate(self.user)
        self.assertEqual(self.client.post("/api/bookings/", self.payload, format="json").status_code, 201)
        response = self.client.get("/api/bookings/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json()), 1)

    def test_double_booking_rejected(self):
        self.client.force_authenticate(self.user)
        self.client.post("/api/bookings/", self.payload, format="json")
        response = self.client.post("/api/bookings/", self.payload, format="json")
        self.assertEqual(response.status_code, 400)

    def test_update_and_delete_booking(self):
        self.client.force_authenticate(self.user)
        pk = self.client.post("/api/bookings/", self.payload, format="json").json()["id"]
        self.payload["reservation_slot"] = 20
        self.assertEqual(self.client.put(f"/api/bookings/{pk}/", self.payload, format="json").status_code, 200)
        self.assertEqual(self.client.delete(f"/api/bookings/{pk}/").status_code, 204)


class AuthTests(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_registration_returns_token(self):
        response = self.client.post(
            "/api/registration/",
            {"username": "newuser", "email": "n@example.com", "password": "StrongPass!234"},
            format="json",
        )
        self.assertEqual(response.status_code, 201)
        self.assertIn("token", response.json())
        self.assertNotIn("password", response.json())

    def test_weak_password_rejected(self):
        response = self.client.post(
            "/api/registration/", {"username": "weak", "password": "123"}, format="json"
        )
        self.assertEqual(response.status_code, 400)

    def test_login_token_and_protected_endpoint(self):
        User.objects.create_user("login", password="StrongPass!234")
        token = self.client.post(
            "/api/token/", {"username": "login", "password": "StrongPass!234"}, format="json"
        ).json()["token"]
        self.assertEqual(self.client.get("/api/me/").status_code, 401)
        self.client.credentials(HTTP_AUTHORIZATION=f"Token {token}")
        response = self.client.get("/api/me/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["username"], "login")
