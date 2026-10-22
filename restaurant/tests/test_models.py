from datetime import date
from decimal import Decimal

from django.test import TestCase

from restaurant.models import Booking, Menu
from restaurant.serializers import MenuSerializer


class MenuModelTest(TestCase):
    def test_menu_str(self):
        item = Menu.objects.create(title="IceCream", price=Decimal("80.00"), inventory=100)
        self.assertEqual(str(item), "IceCream : 80.00")

    def test_menu_fields_saved(self):
        item = Menu.objects.create(title="Pasta", price=Decimal("15.00"), inventory=10)
        saved = Menu.objects.get(pk=item.pk)
        self.assertEqual(saved.title, "Pasta")
        self.assertEqual(saved.inventory, 10)

    def test_menu_serializer_output(self):
        item = Menu.objects.create(title="Greek Salad", price=Decimal("12.50"), inventory=20)
        data = MenuSerializer(item).data
        self.assertEqual(data["title"], "Greek Salad")
        self.assertEqual(data["price"], "12.50")
        self.assertEqual(data["inventory"], 20)


class BookingModelTest(TestCase):
    def test_booking_str(self):
        booking = Booking.objects.create(
            first_name="Ana", reservation_date=date(2026, 11, 1), reservation_slot=18
        )
        self.assertEqual(str(booking), "Ana - 2026-11-01 @ 18:00")

    def test_default_slot(self):
        booking = Booking.objects.create(first_name="Bo", reservation_date=date(2026, 11, 2))
        self.assertEqual(booking.reservation_slot, 10)
