from decimal import Decimal

from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse
from rest_framework.authtoken.models import Token
from rest_framework.test import APIClient

from restaurant.models import Booking, Menu


class StaticPageTest(TestCase):
    def test_pages_render_html(self):
        for name in ("home", "about", "menu-page", "book"):
            response = self.client.get(reverse(name))
            self.assertEqual(response.status_code, 200)
            self.assertContains(response, "Little Lemon")

    def test_menu_page_lists_items(self):
        Menu.objects.create(title="Bruschetta", price=Decimal("7.00"), inventory=5)
        self.assertContains(self.client.get(reverse("menu-page")), "Bruschetta")


class MenuAPITest(TestCase):
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


class BookingAPITest(TestCase):
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
        self.assertEqual(Booking.objects.count(), 1)

    def test_update_and_delete_booking(self):
        self.client.force_authenticate(self.user)
        pk = self.client.post("/api/bookings/", self.payload, format="json").json()["id"]
        self.payload["reservation_slot"] = 20
        self.assertEqual(self.client.put(f"/api/bookings/{pk}/", self.payload, format="json").status_code, 200)
        self.assertEqual(self.client.delete(f"/api/bookings/{pk}/").status_code, 204)


class AuthTest(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_djoser_registration(self):
        response = self.client.post(
            "/auth/users/",
            {"username": "newuser", "email": "n@example.com", "password": "StrongPass!234"},
            format="json",
        )
        self.assertEqual(response.status_code, 201)
        self.assertTrue(User.objects.filter(username="newuser").exists())

    def test_weak_password_rejected(self):
        response = self.client.post(
            "/auth/users/", {"username": "weak", "password": "123"}, format="json"
        )
        self.assertEqual(response.status_code, 400)

    def test_djoser_token_login_and_protected_endpoint(self):
        User.objects.create_user("login", password="StrongPass!234")
        response = self.client.post(
            "/auth/token/login/", {"username": "login", "password": "StrongPass!234"}, format="json"
        )
        self.assertEqual(response.status_code, 200)
        token = response.json()["auth_token"]
        self.assertEqual(self.client.get("/api/me/").status_code, 401)
        self.client.credentials(HTTP_AUTHORIZATION=f"Token {token}")
        me = self.client.get("/api/me/")
        self.assertEqual(me.status_code, 200)
        self.assertEqual(me.json()["username"], "login")

    def test_api_token_auth(self):
        User.objects.create_user("tok", password="StrongPass!234")
        response = self.client.post(
            "/api-token-auth/", {"username": "tok", "password": "StrongPass!234"}, format="json"
        )
        self.assertEqual(response.status_code, 200)
        self.assertIn("token", response.json())
